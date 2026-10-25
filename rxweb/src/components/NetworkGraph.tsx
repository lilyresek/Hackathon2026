import React, { useEffect, useRef, useState, useImperativeHandle, forwardRef, useCallback } from 'react';
import { Network, Options } from 'vis-network';
import { DataSet } from 'vis-data';
import { Drug, DrugInteraction, DRUG_CLASSES } from '../data/drugData';
import {
  ZoomIn,
  ZoomOut,
  Maximize2,
  RotateCcw,
  Play,
  Pause,
  Filter,
  Search,
  Sparkles,
  Info,
  Radio,
  ArrowLeft,
  ArrowRight,
  ShieldAlert,
  Layers,
  Compass,
  CheckCircle2
} from 'lucide-react';

interface NetworkGraphProps {
  drugs: Drug[];
  interactions: DrugInteraction[];
  centerDrugId: string;
  onCenterDrug: (drugId: string) => void;
  onSelectDrug: (drug: Drug | null) => void;
  onSelectInteraction: (interaction: DrugInteraction | null) => void;
  selectedDrugId: string | null;
  cabinetDrugIds: string[];
  isCabinetHighlightActive: boolean;
  onClearCabinetHighlight: () => void;
  historyTrail: string[];
  historyIndex: number;
  onNavigateBack: () => void;
  onNavigateForward: () => void;
  onJumpToHistory: (index: number) => void;
}

export interface NetworkGraphHandle {
  focusDrug: (drugId: string) => void;
  focusInteraction: (drugAId: string, drugBId: string) => void;
  resetView: () => void;
}

export const NetworkGraph = forwardRef<NetworkGraphHandle, NetworkGraphProps>(({
  drugs,
  interactions,
  centerDrugId,
  onCenterDrug,
  onSelectDrug,
  onSelectInteraction,
  selectedDrugId,
  cabinetDrugIds,
  isCabinetHighlightActive,
  onClearCabinetHighlight,
  historyTrail,
  historyIndex,
  onNavigateBack,
  onNavigateForward,
  onJumpToHistory,
}, ref) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const nodesDataSetRef = useRef<DataSet<any> | null>(null);
  const edgesDataSetRef = useRef<DataSet<any> | null>(null);

  // Layout & Physics state
  const [physicsRunning, setPhysicsRunning] = useState<boolean>(false);
  const [springLength, setSpringLength] = useState<number>(180);
  const [repulsionStrength, setRepulsionStrength] = useState<number>(-1200);
  const [physicsPanelOpen, setPhysicsPanelOpen] = useState<boolean>(false);
  const [showCrossLinks, setShowCrossLinks] = useState<boolean>(true);
  const [severityFilter, setSeverityFilter] = useState<'all' | 'severe' | 'moderate'>('all');

  // In-canvas quick search state
  const [canvasSearchQuery, setCanvasSearchQuery] = useState<string>('');
  const [isSearchOpen, setIsSearchOpen] = useState<boolean>(false);

  // Current center drug object
  const centerDrug = drugs.find((d) => d.id === centerDrugId) || drugs[0] || {
    id: 'warfarin',
    brandName: 'Warfarin',
    genericName: 'Warfarin Sodium',
    category: 'Anticoagulant',
    classKey: 'anticoagulant',
    description: '',
    commonSideEffects: [],
    patientAdvice: ''
  };

  // Helper colors
  const getSeverityColor = (severity: 'severe' | 'moderate' | 'minor') => {
    switch (severity) {
      case 'severe':
        return '#EF4444'; // Red
      case 'moderate':
        return '#F97316'; // Orange
      case 'minor':
        return '#EAB308'; // Amber/Yellow
    }
  };

  const getClassColor = (classKey: Drug['classKey']) => {
    const item = DRUG_CLASSES.find((c) => c.key === classKey);
    return item ? item.color : '#0284C7';
  };

  // Build Visual Thesaurus Radial Nodes and Edges
  const buildVisualThesaurusGraph = useCallback(() => {
    // 1. Find all negative interactions involving the central drug
    let directInteractions = interactions.filter(
      (i) => i.drug1 === centerDrug.id || i.drug2 === centerDrug.id
    );

    // Apply severity filter if set
    if (severityFilter !== 'all') {
      directInteractions = directInteractions.filter((i) => i.severity === severityFilter);
    }

    // 2. Map unique spoke drugs radiating from the center
    const spokeMap = new Map<string, { drug: Drug; interaction: DrugInteraction }>();
    directInteractions.forEach((inter) => {
      const otherId = inter.drug1 === centerDrug.id ? inter.drug2 : inter.drug1;
      const otherDrug = drugs.find((d) => d.id === otherId);
      if (otherDrug && !spokeMap.has(otherId)) {
        spokeMap.set(otherId, { drug: otherDrug, interaction: inter });
      }
    });

    const spokeList = Array.from(spokeMap.values());
    const N = spokeList.length;

    // 3. Central Focus Node: Fixed precisely at (0, 0) in prominent circle
    const centerColor = getClassColor(centerDrug.classKey);
    const isCenterInCabinet = cabinetDrugIds.includes(centerDrug.id);

    const centerNode = {
      id: centerDrug.id,
      x: 0,
      y: 0,
      fixed: { x: true, y: true },
      shape: 'circle',
      size: 42,
      label: centerDrug.brandName, // STRICT PLAIN TEXT (Zero HTML tags)
      title: `[Center Focus Node]\n${centerDrug.brandName} (${centerDrug.genericName})\nCategory: ${centerDrug.category}\n${N} radiating negative interaction spokes\nClick to inspect clinical details`,
      color: {
        background: isCenterInCabinet ? '#BE123C' : centerColor,
        border: isCenterInCabinet ? '#9F1239' : '#0369A1',
        highlight: {
          background: isCenterInCabinet ? '#9F1239' : '#0284C7',
          border: '#0F172A',
        },
      },
      font: {
        color: '#FFFFFF',
        size: 14,
        face: 'Plus Jakarta Sans, system-ui, sans-serif',
        bold: true,
      },
      borderWidth: 3.5,
      shadow: {
        enabled: true,
        color: isCenterInCabinet ? 'rgba(190, 18, 60, 0.45)' : 'rgba(2, 132, 199, 0.45)',
        size: 18,
        x: 0,
        y: 4,
      },
      data: centerDrug,
      isCenter: true,
    };

    // 4. Radial Spoke Nodes
    const radius = N > 14 ? 260 : N > 8 ? 220 : 180;
    const spokeNodes = spokeList.map((spoke, idx) => {
      const angle = (2 * Math.PI * idx) / Math.max(1, N) - Math.PI / 2; // Begin at 12 o'clock
      const initX = Math.round(radius * Math.cos(angle));
      const initY = Math.round(radius * Math.sin(angle));

      const isSpokeInCabinet = cabinetDrugIds.includes(spoke.drug.id);
      const sevColor = getSeverityColor(spoke.interaction.severity);

      return {
        id: spoke.drug.id,
        x: initX,
        y: initY,
        shape: 'circle',
        size: isSpokeInCabinet ? 32 : 28,
        label: spoke.drug.brandName, // STRICT PLAIN TEXT
        title: `[Click to Re-Center Web]\n${spoke.drug.brandName} (${spoke.drug.genericName})\nCategory: ${spoke.drug.category}\nInteraction with ${centerDrug.brandName}: ${spoke.interaction.severity.toUpperCase()}\n${spoke.interaction.title}${isSpokeInCabinet ? '\n★ SAVED IN YOUR PRESCRIPTIONS CABINET' : ''}`,
        color: {
          background: isSpokeInCabinet ? '#FFF1F2' : '#FFFFFF',
          border: isSpokeInCabinet ? '#E11D48' : sevColor,
          highlight: {
            background: isSpokeInCabinet ? '#FFE4E6' : '#F0F9FF',
            border: '#0284C7',
          },
          hover: {
            background: '#F8FAFC',
            border: '#0284C7',
          },
        },
        font: {
          color: isSpokeInCabinet ? '#9F1239' : '#0F172A',
          size: 11,
          face: 'Plus Jakarta Sans, system-ui, sans-serif',
          bold: true,
        },
        borderWidth: isSpokeInCabinet ? 3 : 2,
        shadow: {
          enabled: true,
          color: isSpokeInCabinet ? 'rgba(225, 29, 72, 0.25)' : 'rgba(15, 23, 42, 0.08)',
          size: isSpokeInCabinet ? 10 : 5,
          x: 0,
          y: 2,
        },
        data: spoke.drug,
        interactionWithCenter: spoke.interaction,
        isCenter: false,
      };
    });

    const allNodes = [centerNode, ...spokeNodes];

    // 5. Radial Vectors / Edges (From center to each spoke)
    const radialEdges = spokeList.map((spoke) => {
      const sevColor = getSeverityColor(spoke.interaction.severity);
      const isSynergistic = spoke.interaction.mechanismType === 'synergistic';
      const isMetabolic = spoke.interaction.mechanismType === 'metabolic';

      return {
        id: `center-${spoke.interaction.id}`,
        from: centerDrug.id,
        to: spoke.drug.id,
        title: `${spoke.interaction.title}\nSeverity: ${spoke.interaction.severity.toUpperCase()}\nMechanism: ${spoke.interaction.mechanismType}\nClick to view clinical rationale`,
        color: {
          color: sevColor,
          highlight: sevColor,
          hover: '#0284C7',
          opacity: 0.9,
        },
        width: isSynergistic ? 3.5 : 2.5,
        dashes: isMetabolic ? [6, 4] : spoke.interaction.mechanismType === 'clearance' ? [2, 3] : false,
        smooth: {
          enabled: true,
          type: 'curvedCW',
          roundness: 0.08,
        },
        hoverWidth: 2,
        selectionWidth: 2,
        data: spoke.interaction,
        isRadial: true,
      };
    });

    // 6. Cross-Interactions between Spokes (Peripheral Arcs, like Visual Thesaurus secondary links)
    const crossEdges: any[] = [];
    if (showCrossLinks && N > 1) {
      const spokeIdSet = new Set(spokeList.map((s) => s.drug.id));
      const seenCrossPairs = new Set<string>();

      interactions.forEach((inter) => {
        if (inter.drug1 !== centerDrug.id && inter.drug2 !== centerDrug.id) {
          if (spokeIdSet.has(inter.drug1) && spokeIdSet.has(inter.drug2)) {
            const pairKey = [inter.drug1, inter.drug2].sort().join(':::');
            if (!seenCrossPairs.has(pairKey)) {
              seenCrossPairs.add(pairKey);
              const crossColor = getSeverityColor(inter.severity);

              crossEdges.push({
                id: `cross-${inter.id}`,
                from: inter.drug1,
                to: inter.drug2,
                title: `[Cross-Conflict between Spokes]\n${inter.title}\nSeverity: ${inter.severity.toUpperCase()}\nBoth medications interact with each other in addition to ${centerDrug.brandName}`,
                color: {
                  color: crossColor,
                  opacity: 0.4,
                  hover: crossColor,
                },
                width: 1.5,
                dashes: [4, 4],
                smooth: {
                  enabled: true,
                  type: 'curvedCCW',
                  roundness: 0.22,
                },
                hoverWidth: 1.5,
                data: inter,
                isRadial: false,
              });
            }
          }
        }
      });
    }

    const allEdges = [...radialEdges, ...crossEdges];
    return { nodes: allNodes, edges: allEdges, spokeCount: N };
  }, [centerDrug, drugs, interactions, cabinetDrugIds, severityFilter, showCrossLinks]);

  // Initialize and update vis network
  useEffect(() => {
    if (!containerRef.current) return;

    const { nodes, edges } = buildVisualThesaurusGraph();
    const nodesDataSet = new DataSet(nodes);
    const edgesDataSet = new DataSet(edges);

    nodesDataSetRef.current = nodesDataSet;
    edgesDataSetRef.current = edgesDataSet;

    const options: Options = {
      nodes: {
        borderWidthSelected: 3,
      },
      edges: {
        selectionWidth: 2,
      },
      physics: {
        enabled: true,
        solver: 'barnesHut',
        minVelocity: 0.75,
        maxVelocity: 22,
        timestep: 0.5,
        barnesHut: {
          gravitationalConstant: repulsionStrength,
          centralGravity: 0.2,
          springLength: springLength,
          springConstant: 0.04,
          damping: 0.55, // Calms oscillations rapidly
          avoidOverlap: 0.65,
        },
        stabilization: {
          enabled: true,
          iterations: 150, // Rapid radial settling
          updateInterval: 25,
          fit: true,
        },
      },
      interaction: {
        hover: true,
        hoverConnectedEdges: true,
        tooltipDelay: 100,
        dragNodes: true,
        dragView: true,
        zoomView: true,
      },
    };

    const net = new Network(
      containerRef.current,
      { nodes: nodesDataSet as any, edges: edgesDataSet as any },
      options
    );
    networkRef.current = net;

    // Freeze physics once initial radial placement stabilizes
    net.once('stabilized', () => {
      net.setOptions({ physics: { enabled: false } });
      setPhysicsRunning(false);
    });

    net.once('stabilizationIterationsDone', () => {
      net.setOptions({ physics: { enabled: false } });
      setPhysicsRunning(false);
    });

    // Click handler for Visual Thesaurus re-centering & inspection
    net.on('click', (params) => {
      if (params.nodes && params.nodes.length > 0) {
        const clickedNodeId = params.nodes[0] as string;

        if (clickedNodeId === centerDrug.id) {
          // Clicked central drug: inspect it in the sidebar
          onSelectDrug(centerDrug);
        } else {
          // Clicked a spoke drug: Visual Thesaurus re-center transition!
          const spokeDrug = drugs.find((d) => d.id === clickedNodeId);
          if (spokeDrug) {
            // First animate toward the clicked node
            try {
              const nodePos = net.getPosition(clickedNodeId);
              net.moveTo({
                position: nodePos,
                scale: 1.15,
                animation: {
                  duration: 250,
                  easingFunction: 'easeInOutQuad',
                },
              });
            } catch (e) {
              // fallback
            }

            // Then center on that drug
            setTimeout(() => {
              onCenterDrug(clickedNodeId);
              onSelectDrug(spokeDrug);
            }, 180);
          }
        }
      } else if (params.edges && params.edges.length > 0) {
        const clickedEdgeId = params.edges[0] as string;
        const edgeItem = edgesDataSet.get(clickedEdgeId);
        if (edgeItem && edgeItem.data) {
          onSelectInteraction(edgeItem.data);
        }
      }
    });

    // Cleanup on unmount or re-render
    return () => {
      net.destroy();
      networkRef.current = null;
    };
  }, [centerDrugId, buildVisualThesaurusGraph, onCenterDrug, onSelectDrug, onSelectInteraction]);

  // Imperative handles
  useImperativeHandle(ref, () => ({
    focusDrug: (drugId: string) => {
      onCenterDrug(drugId);
    },
    focusInteraction: (drugAId: string, drugBId: string) => {
      if (centerDrug.id !== drugAId && centerDrug.id !== drugBId) {
        onCenterDrug(drugAId);
      }
      setTimeout(() => {
        if (networkRef.current && edgesDataSetRef.current) {
          const matched = interactions.find(
            (i) =>
              (i.drug1 === drugAId && i.drug2 === drugBId) ||
              (i.drug1 === drugBId && i.drug2 === drugAId)
          );
          if (matched) {
            onSelectInteraction(matched);
          }
        }
      }, 300);
    },
    resetView: () => {
      if (networkRef.current) {
        networkRef.current.moveTo({
          position: { x: 0, y: 0 },
          scale: 1.0,
          animation: { duration: 400, easingFunction: 'easeInOutQuad' },
        });
      }
    },
  }));

  // Toggle physics running state
  const handleTogglePhysics = () => {
    if (!networkRef.current) return;
    const nextState = !physicsRunning;
    networkRef.current.setOptions({ physics: { enabled: nextState } });
    setPhysicsRunning(nextState);
  };

  const handleZoomIn = () => {
    if (networkRef.current) {
      networkRef.current.moveTo({ scale: networkRef.current.getScale() * 1.25 });
    }
  };

  const handleZoomOut = () => {
    if (networkRef.current) {
      networkRef.current.moveTo({ scale: networkRef.current.getScale() * 0.8 });
    }
  };

  const handleFit = () => {
    if (networkRef.current) {
      networkRef.current.moveTo({
        position: { x: 0, y: 0 },
        scale: 1.0,
        animation: { duration: 400, easingFunction: 'easeInOutQuad' },
      });
    }
  };

  // Find active conflicts on screen with patient's cabinet
  const onScreenCabinetConflicts = interactions.filter(
    (i) =>
      (i.drug1 === centerDrug.id && cabinetDrugIds.includes(i.drug2)) ||
      (i.drug2 === centerDrug.id && cabinetDrugIds.includes(i.drug1))
  );

  // Autocomplete matching for in-canvas search
  const filteredSuggestions = canvasSearchQuery.trim()
    ? drugs.filter(
        (d) =>
          d.brandName.toLowerCase().includes(canvasSearchQuery.toLowerCase()) ||
          d.genericName.toLowerCase().includes(canvasSearchQuery.toLowerCase())
      ).slice(0, 8)
    : [];

  return (
    <div className="relative w-full h-full bg-[#F8FAFC] overflow-hidden select-none">
      {/* 1. Visual Thesaurus Top Explorer Bar (History Trail & Re-centering Breadcrumbs) */}
      <div className="absolute top-3 left-4 right-4 z-20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pointer-events-none">
        {/* Left: History Trail & Breadcrumbs Navigation */}
        <div className="flex items-center gap-2 pointer-events-auto bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-2xl border border-slate-200 shadow-xs text-xs">
          {/* Back Button */}
          <button
            onClick={onNavigateBack}
            disabled={historyIndex <= 0}
            title="Go back to previous medication (Browser History Back)"
            className={`p-1.5 rounded-lg border flex items-center gap-1 font-semibold transition-all ${
              historyIndex > 0
                ? 'bg-slate-100 hover:bg-slate-200 text-slate-800 border-slate-300'
                : 'bg-slate-50 text-slate-300 border-slate-200 cursor-not-allowed'
            }`}
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span className="hidden md:inline">Back</span>
          </button>

          {/* Forward Button */}
          <button
            onClick={onNavigateForward}
            disabled={historyIndex >= historyTrail.length - 1}
            title="Go forward (Browser History Forward)"
            className={`p-1.5 rounded-lg border flex items-center gap-1 font-semibold transition-all ${
              historyIndex < historyTrail.length - 1
                ? 'bg-slate-100 hover:bg-slate-200 text-slate-800 border-slate-300'
                : 'bg-slate-50 text-slate-300 border-slate-200 cursor-not-allowed'
            }`}
          >
            <span className="hidden md:inline">Forward</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>

          <span className="w-px h-4 bg-slate-200 mx-1" aria-hidden="true" />

          {/* Breadcrumbs Trail */}
          <div className="flex items-center gap-1 text-[11px] overflow-x-auto max-w-xs md:max-w-md py-0.5">
            <span className="text-slate-400 font-medium">Path:</span>
            {historyTrail.slice(Math.max(0, historyTrail.length - 4)).map((histId, idx, arr) => {
              const histDrug = drugs.find((d) => d.id === histId);
              if (!histDrug) return null;
              const isCurrent = histId === centerDrug.id;

              return (
                <React.Fragment key={`${histId}-${idx}`}>
                  <button
                    onClick={() => onCenterDrug(histDrug.id)}
                    className={`px-2 py-0.5 rounded-md font-semibold transition-colors ${
                      isCurrent
                        ? 'bg-sky-100 text-sky-800 border border-sky-300 shadow-2xs'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    {histDrug.brandName}
                  </button>
                  {idx < arr.length - 1 && (
                    <span className="text-slate-300 font-bold">›</span>
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </div>

        {/* Right: Quick Canvas Controls (Zoom, Fit, Physics Drawer, Filter) */}
        <div className="flex items-center gap-2 pointer-events-auto">
          {/* Severity filter toggle */}
          <div className="bg-white/95 backdrop-blur-md border border-slate-200 rounded-xl p-1 shadow-xs flex items-center text-[11px]">
            <button
              onClick={() => setSeverityFilter('all')}
              className={`px-2 py-1 rounded-lg font-semibold transition-colors ${
                severityFilter === 'all'
                  ? 'bg-slate-900 text-white'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Risks
            </button>
            <button
              onClick={() => setSeverityFilter('severe')}
              className={`px-2 py-1 rounded-lg font-semibold transition-colors ${
                severityFilter === 'severe'
                  ? 'bg-rose-600 text-white'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Severe Only
            </button>
          </div>

          {/* Cross-links toggle */}
          <button
            onClick={() => setShowCrossLinks(!showCrossLinks)}
            title="Toggle cross-conflict links between surrounding spokes"
            className={`px-2.5 py-1.5 text-xs font-semibold rounded-xl border transition-all shadow-xs flex items-center gap-1.5 ${
              showCrossLinks
                ? 'bg-white/95 border-sky-300 text-sky-800'
                : 'bg-slate-100 border-slate-200 text-slate-500'
            }`}
          >
            <Layers className="w-3.5 h-3.5 text-sky-600" />
            <span className="hidden sm:inline">Cross Links</span>
          </button>

          {/* Zoom & Fit controls */}
          <div className="bg-white/95 backdrop-blur-md border border-slate-200 rounded-xl p-1 shadow-xs flex items-center gap-0.5 text-xs">
            <button
              onClick={handleZoomIn}
              className="p-1 hover:bg-slate-100 rounded text-slate-700"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleZoomOut}
              className="p-1 hover:bg-slate-100 rounded text-slate-700"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleFit}
              className="px-2 py-1 hover:bg-slate-100 rounded text-[11px] font-semibold text-slate-700"
              title="Center View"
            >
              Recenter
            </button>
          </div>
        </div>
      </div>

      {/* 2. Visual Thesaurus Center Indicator Banner */}
      <div className="absolute bottom-4 right-4 z-20 pointer-events-auto bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-3 shadow-md max-w-xs text-xs space-y-1.5">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-bold uppercase tracking-wider text-sky-700 flex items-center gap-1">
            <Compass className="w-3.5 h-3.5 text-sky-600" />
            Visual Thesaurus Radial Web
          </span>
          <span className="text-[10px] text-slate-400">Click any spoke to jump</span>
        </div>
        <div className="font-bold text-sm text-slate-900 flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-sky-600 inline-block" />
          <span>{centerDrug.brandName}</span>
          <span className="text-xs text-slate-400 font-normal">({centerDrug.genericName})</span>
        </div>
        <p className="text-[11px] text-slate-500 leading-tight">
          Click any orbiting node to navigate the interaction map, or click a branch line to view pharmacological mechanism.
        </p>
      </div>

      {/* 3. Cabinet Conflict Alert Banner (If center drug conflicts with patient cabinet) */}
      {onScreenCabinetConflicts.length > 0 && (
        <div className="absolute top-16 left-4 z-20 pointer-events-auto bg-rose-50/95 backdrop-blur-md border border-rose-300 rounded-2xl p-3 shadow-lg max-w-sm text-xs">
          <div className="flex items-center gap-1.5 text-rose-800 font-bold text-xs mb-1">
            <ShieldAlert className="w-4 h-4 text-rose-600 shrink-0" />
            <span>Prescription Cabinet Alert ({onScreenCabinetConflicts.length})</span>
          </div>
          <div className="text-[11px] text-rose-950 leading-snug space-y-1">
            {onScreenCabinetConflicts.map((c) => {
              const conflictingDrugId = c.drug1 === centerDrug.id ? c.drug2 : c.drug1;
              const conflictDrug = drugs.find((d) => d.id === conflictingDrugId);
              return (
                <div key={c.id} className="flex items-center justify-between">
                  <span>
                    <strong>{centerDrug.brandName}</strong> interacts with <strong>{conflictDrug?.brandName}</strong> ({c.severity.toUpperCase()})
                  </span>
                  <button
                    onClick={() => onSelectInteraction(c)}
                    className="underline text-rose-700 font-semibold hover:text-rose-900 ml-2"
                  >
                    View
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 4. Visual Thesaurus Legend */}
      <div className="absolute bottom-4 left-4 z-20 pointer-events-auto bg-white/95 backdrop-blur-md border border-slate-200/90 rounded-2xl p-3 shadow-md text-xs space-y-1.5 max-w-xs">
        <div className="font-bold text-[11px] uppercase tracking-wider text-slate-700">
          Interaction Severity Vectors
        </div>
        <div className="flex items-center gap-3 text-[11px] text-slate-600">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
            Severe
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-orange-500" />
            Moderate
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
            Minor
          </span>
        </div>
        <div className="flex items-center gap-3 text-[10px] text-slate-500 pt-1 border-t border-slate-100">
          <span>— Synergistic (Solid)</span>
          <span>- - Metabolic (Dashed)</span>
        </div>
      </div>

      {/* 5. vis-network Container */}
      <div ref={containerRef} className="w-full h-full" />
    </div>
  );
});
