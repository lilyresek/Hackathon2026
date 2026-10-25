import React, { useState, useRef, useEffect } from 'react';
import {
  DRUGS,
  INTERACTIONS,
  PRESET_DATASETS,
  PresetDataset,
  findInteractionsInCabinet,
  Drug,
  DrugInteraction,
} from './data/drugData';
import { NetworkGraph, NetworkGraphHandle } from './components/NetworkGraph';
import { DrugInfoSidebar } from './components/DrugInfoSidebar';
import { InteractionChecker } from './components/InteractionChecker';
import { PrescriptionCabinet } from './components/PrescriptionCabinet';
import { DatasetManagerModal } from './components/DatasetManagerModal';
import { SingleHtmlExportModal } from './components/SingleHtmlExportModal';
import {
  ShieldAlert,
  Search,
  Database,
  FileCode,
  HeartPulse,
  Info,
  CheckCircle2,
  Sparkles,
  BookOpen,
  X,
  Compass,
  ArrowLeft,
  ArrowRight
} from 'lucide-react';

export default function App() {
  const graphRef = useRef<NetworkGraphHandle>(null);

  // Active Dataset state
  const [activeDatasetId, setActiveDatasetId] = useState<string>('default-all');
  const [currentDrugs, setCurrentDrugs] = useState<Drug[]>(DRUGS);
  const [currentInteractions, setCurrentInteractions] = useState<DrugInteraction[]>(INTERACTIONS);

  // Visual Thesaurus Central Focus & History State
  const getInitialDrugId = (): string => {
    if (typeof window !== 'undefined' && window.location.hash.startsWith('#drug=')) {
      const hashId = window.location.hash.replace('#drug=', '').toLowerCase();
      const match = DRUGS.find((d) => d.id === hashId);
      if (match) return match.id;
    }
    return 'warfarin';
  };

  const [centerDrugId, setCenterDrugId] = useState<string>(getInitialDrugId);
  const [historyTrail, setHistoryTrail] = useState<string[]>([getInitialDrugId()]);
  const [historyIndex, setHistoryIndex] = useState<number>(0);

  // Selected entities for detail sidebar
  const [selectedDrug, setSelectedDrug] = useState<Drug | null>(null);
  const [selectedInteraction, setSelectedInteraction] = useState<DrugInteraction | null>(null);

  // Patient Cabinet state
  const [cabinetDrugIds, setCabinetDrugIds] = useState<string[]>(['warfarin', 'aspirin', 'lipitor']);
  const [isCabinetHighlightActive, setIsCabinetHighlightActive] = useState<boolean>(false);

  // Top Search Bar State
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isSearchDropdownOpen, setIsSearchDropdownOpen] = useState<boolean>(false);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Modals state
  const [isCheckerOpen, setIsCheckerOpen] = useState<boolean>(false);
  const [isCabinetOpen, setIsCabinetOpen] = useState<boolean>(false);
  const [isDatasetManagerOpen, setIsDatasetManagerOpen] = useState<boolean>(false);
  const [isExportOpen, setIsExportOpen] = useState<boolean>(false);

  // Compute active center drug
  const currentCenterDrug = currentDrugs.find((d) => d.id === centerDrugId) || currentDrugs[0];

  // Compute cabinet conflicts in real-time
  const cabinetEvaluation = findInteractionsInCabinet(cabinetDrugIds, currentDrugs, currentInteractions);
  const hasCabinetConflicts = cabinetEvaluation.conflicts.length > 0;

  // Sync with browser URL hash & forward/back button navigation
  useEffect(() => {
    const handleHashChange = () => {
      if (window.location.hash.startsWith('#drug=')) {
        const drugId = window.location.hash.replace('#drug=', '').toLowerCase();
        if (drugId !== centerDrugId && currentDrugs.some((d) => d.id === drugId)) {
          setCenterDrugId(drugId);
        }
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [centerDrugId, currentDrugs]);

  // Center on a new drug (Visual Thesaurus re-center transition)
  const handleCenterDrug = (drugId: string) => {
    if (drugId === centerDrugId) return;
    const targetDrug = currentDrugs.find((d) => d.id === drugId);
    if (!targetDrug) return;

    // Update history trail (drop forward history if branching)
    const newTrail = historyTrail.slice(0, historyIndex + 1);
    newTrail.push(drugId);
    setHistoryTrail(newTrail);
    setHistoryIndex(newTrail.length - 1);

    setCenterDrugId(drugId);
    setSelectedDrug(targetDrug);
    setSelectedInteraction(null);

    // Update URL hash
    window.location.hash = `#drug=${drugId}`;
  };

  // History Navigation: Back
  const handleNavigateBack = () => {
    if (historyIndex > 0) {
      const nextIndex = historyIndex - 1;
      const targetId = historyTrail[nextIndex];
      setHistoryIndex(nextIndex);
      setCenterDrugId(targetId);
      setSelectedDrug(currentDrugs.find((d) => d.id === targetId) || null);
      setSelectedInteraction(null);
      window.location.hash = `#drug=${targetId}`;
    }
  };

  // History Navigation: Forward
  const handleNavigateForward = () => {
    if (historyIndex < historyTrail.length - 1) {
      const nextIndex = historyIndex + 1;
      const targetId = historyTrail[nextIndex];
      setHistoryIndex(nextIndex);
      setCenterDrugId(targetId);
      setSelectedDrug(currentDrugs.find((d) => d.id === targetId) || null);
      setSelectedInteraction(null);
      window.location.hash = `#drug=${targetId}`;
    }
  };

  // History Navigation: Jump directly to an index in the breadcrumb trail
  const handleJumpToHistory = (index: number) => {
    if (index >= 0 && index < historyTrail.length) {
      const targetId = historyTrail[index];
      setHistoryIndex(index);
      setCenterDrugId(targetId);
      setSelectedDrug(currentDrugs.find((d) => d.id === targetId) || null);
      setSelectedInteraction(null);
      window.location.hash = `#drug=${targetId}`;
    }
  };

  // Search input change & autocomplete
  const searchResults = searchQuery.trim()
    ? currentDrugs.filter(
        (d) =>
          d.brandName.toLowerCase().includes(searchQuery.toLowerCase()) ||
          d.genericName.toLowerCase().includes(searchQuery.toLowerCase()) ||
          d.category.toLowerCase().includes(searchQuery.toLowerCase())
      ).slice(0, 8)
    : [];

  const handleSelectSearchResult = (drug: Drug) => {
    handleCenterDrug(drug.id);
    setSearchQuery('');
    setIsSearchDropdownOpen(false);
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && searchResults.length > 0) {
      handleSelectSearchResult(searchResults[0]);
    } else if (e.key === 'Escape') {
      setIsSearchDropdownOpen(false);
    }
  };

  // Handlers for selection
  const handleSelectDrug = (drug: Drug | null) => {
    setSelectedDrug(drug);
    if (drug) setSelectedInteraction(null);
  };

  const handleSelectInteraction = (interaction: DrugInteraction | null) => {
    setSelectedInteraction(interaction);
    if (interaction) setSelectedDrug(null);
  };

  const handleToggleCabinet = (drugId: string) => {
    setCabinetDrugIds((prev) =>
      prev.includes(drugId) ? prev.filter((id) => id !== drugId) : [...prev, drugId]
    );
  };

  const handleClearCabinetHighlight = () => {
    setIsCabinetHighlightActive(false);
    if (graphRef.current) graphRef.current.resetView();
  };

  // Dataset switching handlers
  const handleSelectPreset = (preset: PresetDataset) => {
    setActiveDatasetId(preset.id);
    setCurrentDrugs(preset.drugs);
    setCurrentInteractions(preset.interactions);
    setSelectedDrug(null);
    setSelectedInteraction(null);
    setIsCabinetHighlightActive(false);

    // If active center drug is in new dataset, keep it; otherwise pick first
    const exists = preset.drugs.some((d) => d.id === centerDrugId);
    if (!exists && preset.drugs.length > 0) {
      setCenterDrugId(preset.drugs[0].id);
      setHistoryTrail([preset.drugs[0].id]);
      setHistoryIndex(0);
      window.location.hash = `#drug=${preset.drugs[0].id}`;
    }
  };

  const handleLoadCustomData = (drugs: Drug[], interactions: DrugInteraction[], _name: string) => {
    setActiveDatasetId('custom-upload');
    setCurrentDrugs(drugs);
    setCurrentInteractions(interactions);
    setSelectedDrug(null);
    setSelectedInteraction(null);
    setIsCabinetHighlightActive(false);

    if (drugs.length > 0) {
      setCenterDrugId(drugs[0].id);
      setHistoryTrail([drugs[0].id]);
      setHistoryIndex(0);
      window.location.hash = `#drug=${drugs[0].id}`;
    }
  };

  return (
    <div className="w-screen h-screen flex flex-col bg-[#F8FAFC] text-slate-900 overflow-hidden select-none">
      {/* 
        Top Bar: Visual Thesaurus Style Header
        Brand + Centered Visual Thesaurus Search Bar + Navigation Actions
      */}
      <header className="h-14 bg-white border-b border-slate-200 px-4 md:px-6 flex items-center justify-between gap-4 shrink-0 z-30">
        {/* Brand title */}
        <div className="flex items-center gap-2.5 whitespace-nowrap shrink-0">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-sky-600 to-cyan-500 text-white flex items-center justify-center font-bold text-sm shadow-xs">
            Rx
          </div>
          <span className="text-lg font-bold tracking-tight text-slate-900">
            RxWeb
          </span>
          <span className="text-xs text-slate-400 hidden sm:inline">·</span>
          <span className="text-xs text-slate-500 hidden lg:inline font-medium">
            Visual Thesaurus Radial Map
          </span>
        </div>

        {/* Center: Visual Thesaurus Search Bar */}
        <div className="flex-1 max-w-md relative">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              ref={searchInputRef}
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setIsSearchDropdownOpen(true);
              }}
              onFocus={() => setIsSearchDropdownOpen(true)}
              onKeyDown={handleSearchKeyDown}
              placeholder="Search medication (e.g. Warfarin, Lipitor, Zoloft)..."
              className="w-full text-xs bg-slate-50 border border-slate-200 focus:border-sky-500 focus:bg-white pl-9 pr-8 py-2 rounded-xl outline-none transition-all placeholder:text-slate-400"
            />
            {searchQuery && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setIsSearchDropdownOpen(false);
                }}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Autocomplete Dropdown */}
          {isSearchDropdownOpen && searchResults.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-xl shadow-xl z-50 overflow-hidden divide-y divide-slate-100 max-h-72 overflow-y-auto">
              {searchResults.map((d) => (
                <button
                  key={d.id}
                  onClick={() => handleSelectSearchResult(d)}
                  className="w-full p-2.5 text-left text-xs hover:bg-sky-50/70 flex items-center justify-between transition-colors group"
                >
                  <div>
                    <div className="font-bold text-slate-900 group-hover:text-sky-700">
                      {d.brandName}
                    </div>
                    <div className="text-[11px] text-slate-500 font-mono">
                      {d.genericName} · {d.category}
                    </div>
                  </div>
                  <span className="text-[10px] text-sky-600 font-semibold group-hover:underline">
                    Center Web →
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right Nav Links & Cabinet Button */}
        <div className="flex items-center gap-3 shrink-0">
          <nav className="hidden lg:flex items-center gap-4 text-xs font-semibold text-slate-600">
            <button
              onClick={() => setIsCheckerOpen(true)}
              className="hover:text-slate-900 transition-colors flex items-center gap-1.5"
            >
              <span>Pair Checker</span>
            </button>
            <button
              onClick={() => setIsDatasetManagerOpen(true)}
              className="hover:text-slate-900 transition-colors flex items-center gap-1.5"
            >
              <span>Datasets</span>
            </button>
            <button
              onClick={() => setIsExportOpen(true)}
              className="hover:text-sky-700 text-sky-600 transition-colors flex items-center gap-1.5"
            >
              <FileCode className="w-3.5 h-3.5" />
              <span>Export HTML</span>
            </button>
          </nav>

          {/* Primary Action: Cabinet Button */}
          <button
            onClick={() => setIsCabinetOpen(true)}
            className={`px-3.5 py-2 text-xs font-semibold rounded-xl transition-all shadow-xs flex items-center gap-2 whitespace-nowrap ${
              hasCabinetConflicts
                ? 'bg-rose-600 text-white hover:bg-rose-700'
                : 'bg-slate-900 text-white hover:bg-slate-800'
            }`}
          >
            {hasCabinetConflicts ? (
              <ShieldAlert className="w-3.5 h-3.5 text-rose-200 animate-pulse" />
            ) : (
              <HeartPulse className="w-3.5 h-3.5 text-sky-300" />
            )}
            <span>My Prescriptions ({cabinetDrugIds.length})</span>
            {hasCabinetConflicts && (
              <span className="w-2 h-2 rounded-full bg-rose-300" />
            )}
          </button>
        </div>
      </header>

      {/* Main Interactive Workspace: Visual Thesaurus Radial Network + Clinical Sidebar */}
      <main className="flex-1 flex overflow-hidden relative">
        {/* Left/Center: Visual Thesaurus Canvas */}
        <section aria-label="Visual Thesaurus Radial Map" className="flex-1 h-full relative">
          <NetworkGraph
            ref={graphRef}
            drugs={currentDrugs}
            interactions={currentInteractions}
            centerDrugId={centerDrugId}
            onCenterDrug={handleCenterDrug}
            onSelectDrug={handleSelectDrug}
            onSelectInteraction={handleSelectInteraction}
            selectedDrugId={selectedDrug?.id || null}
            cabinetDrugIds={cabinetDrugIds}
            isCabinetHighlightActive={isCabinetHighlightActive}
            onClearCabinetHighlight={handleClearCabinetHighlight}
            historyTrail={historyTrail}
            historyIndex={historyIndex}
            onNavigateBack={handleNavigateBack}
            onNavigateForward={handleNavigateForward}
            onJumpToHistory={handleJumpToHistory}
          />
        </section>

        {/* Right: Dynamic Clinical Inspector & Definition Card */}
        <DrugInfoSidebar
          drugs={currentDrugs}
          interactions={currentInteractions}
          centerDrug={currentCenterDrug}
          selectedDrug={selectedDrug}
          selectedInteraction={selectedInteraction}
          onClose={() => {
            setSelectedDrug(null);
            setSelectedInteraction(null);
          }}
          onSelectDrug={handleSelectDrug}
          onCenterDrug={handleCenterDrug}
          onSelectInteraction={handleSelectInteraction}
          isInCabinet={(id) => cabinetDrugIds.includes(id)}
          onToggleCabinet={handleToggleCabinet}
        />
      </main>

      {/* Modals */}
      <InteractionChecker
        isOpen={isCheckerOpen}
        onClose={() => setIsCheckerOpen(false)}
        drugs={currentDrugs}
        interactions={currentInteractions}
        onFocusInteractionOnGraph={(drugAId: string, drugBId: string) => {
          setIsCheckerOpen(false);
          handleCenterDrug(drugAId);
          setTimeout(() => {
            const match = currentInteractions.find(
              (i) =>
                (i.drug1 === drugAId && i.drug2 === drugBId) ||
                (i.drug1 === drugBId && i.drug2 === drugAId)
            );
            if (match) setSelectedInteraction(match);
          }, 350);
        }}
      />

      <PrescriptionCabinet
        isOpen={isCabinetOpen}
        onClose={() => setIsCabinetOpen(false)}
        drugs={currentDrugs}
        interactions={currentInteractions}
        cabinetDrugIds={cabinetDrugIds}
        onAddDrug={(id) => {
          if (!cabinetDrugIds.includes(id)) {
            setCabinetDrugIds((prev) => [...prev, id]);
          }
        }}
        onRemoveDrug={(id) => {
          setCabinetDrugIds((prev) => prev.filter((x) => x !== id));
        }}
        onClearCabinet={() => {
          setCabinetDrugIds([]);
          setIsCabinetHighlightActive(false);
        }}
        onSelectDrug={(d) => {
          setIsCabinetOpen(false);
          handleCenterDrug(d.id);
        }}
        onFocusInteraction={(drugAId, drugBId) => {
          setIsCabinetOpen(false);
          handleCenterDrug(drugAId);
        }}
        onHighlightInGraph={() => {
          setIsCabinetOpen(false);
          setIsCabinetHighlightActive(true);
        }}
        onLoadPreset={(ids) => setCabinetDrugIds(ids)}
      />

      <DatasetManagerModal
        isOpen={isDatasetManagerOpen}
        onClose={() => setIsDatasetManagerOpen(false)}
        activeDatasetId={activeDatasetId}
        onSelectPreset={handleSelectPreset}
        onLoadCustomData={handleLoadCustomData}
        currentDrugs={currentDrugs}
        currentInteractions={currentInteractions}
      />

      <SingleHtmlExportModal
        isOpen={isExportOpen}
        onClose={() => setIsExportOpen(false)}
        drugs={currentDrugs}
        interactions={currentInteractions}
      />
    </div>
  );
}
