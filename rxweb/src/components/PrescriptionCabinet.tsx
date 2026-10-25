import React, { useState } from 'react';
import { DRUGS, INTERACTIONS, findInteractionsInCabinet, Drug, DrugInteraction } from '../data/drugData';
import {
  ShieldAlert,
  ShieldCheck,
  Plus,
  Trash2,
  X,
  Compass,
  AlertTriangle,
  Info,
  Layers,
  Sparkles
} from 'lucide-react';

interface PrescriptionCabinetProps {
  drugs?: Drug[];
  interactions?: DrugInteraction[];
  isOpen: boolean;
  onClose: () => void;
  cabinetDrugIds: string[];
  onAddDrug: (drugId: string) => void;
  onRemoveDrug: (drugId: string) => void;
  onClearCabinet: () => void;
  onLoadPreset: (presetIds: string[]) => void;
  onHighlightInGraph: () => void;
  onFocusInteraction: (drugAId: string, drugBId: string) => void;
  onSelectDrug: (drug: Drug) => void;
}

export const PrescriptionCabinet: React.FC<PrescriptionCabinetProps> = ({
  drugs = DRUGS,
  interactions = INTERACTIONS,
  isOpen,
  onClose,
  cabinetDrugIds,
  onAddDrug,
  onRemoveDrug,
  onClearCabinet,
  onLoadPreset,
  onHighlightInGraph,
  onFocusInteraction,
  onSelectDrug,
}) => {
  const [selectedToAdd, setSelectedToAdd] = useState<string>('');

  if (!isOpen) return null;

  const cabinetDrugs = drugs.filter((d) => cabinetDrugIds.includes(d.id));
  const { conflicts, severeCount, moderateCount, minorCount } = findInteractionsInCabinet(
    cabinetDrugIds,
    drugs,
    interactions
  );

  const availableToAdd = drugs.filter((d) => !cabinetDrugIds.includes(d.id));


  const handleAdd = () => {
    if (!selectedToAdd) return;
    onAddDrug(selectedToAdd);
    setSelectedToAdd('');
  };

  const presets = [
    {
      name: 'Cardiology & Pain Alert',
      desc: 'Warfarin, Aspirin, Lipitor, Diflucan',
      ids: ['warfarin', 'aspirin', 'lipitor', 'diflucan'],
      type: 'danger',
    },
    {
      name: 'Psych & Sleep Alert',
      desc: 'Zoloft, Xanax, Tramadol, Ambien',
      ids: ['zoloft', 'xanax', 'tramadol', 'ambien'],
      type: 'danger',
    },
    {
      name: 'Safe Daily Regimen',
      desc: 'Metformin, Synthroid, Tylenol',
      ids: ['metformin', 'synthroid', 'tylenol'],
      type: 'safe',
    },
  ];

  const hasConflicts = conflicts.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl max-w-2xl w-full border border-slate-200 shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/80">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-base font-bold text-slate-900">
                My Prescription Cabinet
              </h3>
              <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-slate-200/70 text-slate-700">
                {cabinetDrugIds.length} Active
              </span>
            </div>
            <p className="text-xs text-slate-500">
              Real-time multi-drug interaction safety scanner for personal medication lists.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200/60 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 overflow-y-auto space-y-6">
          {/* Real-time Safety Assessment Card */}
          <div
            className={`p-4 rounded-xl border transition-all ${
              hasConflicts
                ? severeCount > 0
                  ? 'bg-rose-50/80 border-rose-300 text-rose-950'
                  : 'bg-orange-50/80 border-orange-300 text-orange-950'
                : cabinetDrugIds.length >= 2
                ? 'bg-emerald-50/80 border-emerald-300 text-emerald-950'
                : 'bg-slate-50 border-slate-200 text-slate-700'
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2.5">
                {hasConflicts ? (
                  <div
                    className={`w-9 h-9 rounded-xl flex items-center justify-center text-white shrink-0 ${
                      severeCount > 0 ? 'bg-rose-600' : 'bg-orange-500'
                    }`}
                  >
                    <ShieldAlert className="w-5 h-5" />
                  </div>
                ) : (
                  <div className="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center text-white shrink-0">
                    <ShieldCheck className="w-5 h-5" />
                  </div>
                )}
                <div>
                  <h4 className="text-sm font-bold">
                    {hasConflicts
                      ? `${conflicts.length} Interaction Cluster${
                          conflicts.length > 1 ? 's' : ''
                        } Detected!`
                      : cabinetDrugIds.length >= 2
                      ? 'Cabinet Safe: No Documented Conflicts'
                      : 'Add at least 2 medications to scan for interactions'}
                  </h4>
                  <div className="text-xs opacity-90 mt-0.5">
                    {hasConflicts ? (
                      <span className="flex items-center gap-2">
                        {severeCount > 0 && (
                          <strong className="text-rose-700">{severeCount} Severe High-Risk</strong>
                        )}
                        {moderateCount > 0 && (
                          <strong className="text-orange-700">{moderateCount} Moderate</strong>
                        )}
                        {minorCount > 0 && (
                          <span className="text-amber-700">{minorCount} Minor</span>
                        )}
                      </span>
                    ) : (
                      'All combinations in this cabinet have no direct high-risk drug-drug clash.'
                    )}
                  </div>
                </div>
              </div>

              {cabinetDrugIds.length >= 2 && (
                <button
                  onClick={() => {
                    onClose();
                    onHighlightInGraph();
                  }}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-800 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors shadow-2xs shrink-0"
                >
                  <Compass className="w-3.5 h-3.5 text-sky-600" />
                  <span>Highlight on Graph</span>
                </button>
              )}
            </div>
          </div>

          {/* Conflict Details Cluster if conflicts exist */}
          {hasConflicts && (
            <div className="space-y-2.5">
              <span className="text-[11px] font-semibold text-rose-800 uppercase tracking-wider block">
                Flagged Hazardous Drug Pairs
              </span>
              <div className="space-y-2">
                {conflicts.map(({ interaction, drugA, drugB }) => {
                  const isSevere = interaction.severity === 'severe';
                  return (
                    <div
                      key={interaction.id}
                      className="p-3.5 bg-white border border-slate-200 rounded-xl shadow-2xs hover:border-slate-300 transition-all space-y-1.5"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider text-white ${
                              isSevere ? 'bg-rose-600' : 'bg-orange-500'
                            }`}
                          >
                            {interaction.severity}
                          </span>
                          <span className="text-xs font-bold text-slate-900">
                            {drugA.brandName} ⇄ {drugB.brandName}
                          </span>
                        </div>
                        <button
                          onClick={() => {
                            onClose();
                            onFocusInteraction(drugA.id, drugB.id);
                          }}
                          className="text-[11px] font-medium text-sky-600 hover:text-sky-800 hover:underline"
                        >
                          View Interaction
                        </button>
                      </div>
                      <div className="text-xs font-semibold text-slate-800">
                        {interaction.title}
                      </div>
                      <p className="text-xs text-slate-600 leading-relaxed">
                        {interaction.description}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Current Saved Drugs List */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                Current Medications ({cabinetDrugs.length})
              </span>
              {cabinetDrugs.length > 0 && (
                <button
                  onClick={onClearCabinet}
                  className="text-xs text-slate-400 hover:text-rose-600 transition-colors flex items-center gap-1"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  Clear All
                </button>
              )}
            </div>

            {cabinetDrugs.length === 0 ? (
              <div className="p-8 text-center bg-slate-50 border border-dashed border-slate-200 rounded-xl text-xs text-slate-500">
                Your prescription cabinet is empty. Add your medications below or choose a clinical sample preset.
              </div>
            ) : (
              <div className="divide-y divide-slate-100 border border-slate-200 rounded-xl overflow-hidden bg-white">
                {cabinetDrugs.map((drug) => (
                  <div
                    key={drug.id}
                    className="p-3 flex items-center justify-between hover:bg-slate-50/70 transition-colors"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => {
                            onClose();
                            onSelectDrug(drug);
                          }}
                          className="text-xs font-bold text-slate-900 hover:text-sky-700 hover:underline text-left"
                        >
                          {drug.brandName}
                        </button>
                        <span className="text-[11px] text-slate-400">·</span>
                        <span className="text-[11px] text-slate-500 font-mono">
                          {drug.genericName}
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-500 mt-0.5">
                        {drug.category}
                      </div>
                    </div>

                    <button
                      onClick={() => onRemoveDrug(drug.id)}
                      title="Remove from cabinet"
                      className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Add Medication Bar */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
            <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider block">
              Add Medication to Cabinet
            </span>
            <div className="flex items-center gap-2">
              <select
                value={selectedToAdd}
                onChange={(e) => setSelectedToAdd(e.target.value)}
                className="flex-1 px-3 py-2 text-xs text-slate-800 bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              >
                <option value="">Select a medication to add...</option>
                {availableToAdd.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.brandName} ({d.genericName}) - {d.category}
                  </option>
                ))}
              </select>
              <button
                onClick={handleAdd}
                disabled={!selectedToAdd}
                className="px-4 py-2 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg transition-colors flex items-center gap-1.5 shrink-0"
              >
                <Plus className="w-3.5 h-3.5" />
                Add
              </button>
            </div>
          </div>

          {/* Quick Presets */}
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              Load Sample Presets to Test Scanner
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {presets.map((preset) => (
                <button
                  key={preset.name}
                  onClick={() => onLoadPreset(preset.ids)}
                  className="p-3 text-left rounded-xl border border-slate-200 hover:border-sky-300 hover:bg-sky-50/50 bg-white transition-all group"
                >
                  <div className="text-xs font-bold text-slate-800 group-hover:text-sky-700">
                    {preset.name}
                  </div>
                  <div className="text-[11px] text-slate-500 truncate mt-0.5">
                    {preset.desc}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1 font-medium">
                    {preset.ids.length} drugs
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
          <div className="text-[11px] text-slate-500">
            Scanning across 24 medications and all documented pairs.
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-lg transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};
