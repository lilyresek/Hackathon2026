import React from 'react';
import { Drug, DrugInteraction, DRUGS, DRUG_CLASSES, INTERACTIONS } from '../data/drugData';
import {
  AlertTriangle,
  ShieldAlert,
  Info,
  Check,
  Plus,
  Trash2,
  X,
  ExternalLink,
  Activity,
  ArrowRight,
  Compass,
  Sparkles
} from 'lucide-react';

interface DrugInfoSidebarProps {
  drugs?: Drug[];
  interactions?: DrugInteraction[];
  centerDrug?: Drug | null;
  selectedDrug: Drug | null;
  selectedInteraction: DrugInteraction | null;
  onClose: () => void;
  onSelectDrug: (drug: Drug) => void;
  onCenterDrug?: (drugId: string) => void;
  onSelectInteraction: (interaction: DrugInteraction) => void;
  isInCabinet: (drugId: string) => boolean;
  onToggleCabinet: (drugId: string) => void;
}

export const DrugInfoSidebar: React.FC<DrugInfoSidebarProps> = ({
  drugs = DRUGS,
  interactions = INTERACTIONS,
  centerDrug,
  selectedDrug,
  selectedInteraction,
  onClose,
  onSelectDrug,
  onCenterDrug,
  onSelectInteraction,
  isInCabinet,
  onToggleCabinet,
}) => {
  // If an interaction line is selected, show its clinical details
  if (selectedInteraction) {
    const drugA = drugs.find((d) => d.id === selectedInteraction.drug1);
    const drugB = drugs.find((d) => d.id === selectedInteraction.drug2);

    const isSevere = selectedInteraction.severity === 'severe';
    const isModerate = selectedInteraction.severity === 'moderate';

    const severityBg = isSevere
      ? 'bg-rose-50 border-rose-200 text-rose-900'
      : isModerate
      ? 'bg-orange-50 border-orange-200 text-orange-900'
      : 'bg-amber-50 border-amber-200 text-amber-900';
    const severityBadge = isSevere
      ? 'bg-rose-600 text-white'
      : isModerate
      ? 'bg-orange-500 text-white'
      : 'bg-amber-500 text-white';

    return (
      <aside
        aria-label="Interaction Details"
        className="w-80 md:w-96 bg-white border-l border-slate-200 h-full flex flex-col shadow-lg z-20 overflow-y-auto"
      >
        {/* Header */}
        <div className="p-4 border-b border-slate-100 flex items-start justify-between bg-slate-50/80">
          <div>
            <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
              <span>Drug-Drug Interaction</span>
              <span aria-hidden="true">·</span>
              <span className="capitalize">{selectedInteraction.mechanismType}</span>
            </div>
            <div className="flex items-center gap-2">
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${severityBadge}`}
              >
                {selectedInteraction.severity} Risk
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200/50 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4 flex-1">
          {/* Drug A & B Pills */}
          <div className="flex items-center justify-between gap-2 p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs">
            <button
              onClick={() => drugA && onSelectDrug(drugA)}
              className="font-bold text-slate-900 hover:text-sky-700 truncate"
            >
              {drugA?.brandName || selectedInteraction.drug1}
            </button>
            <span className="text-slate-400 font-bold">⇄</span>
            <button
              onClick={() => drugB && onSelectDrug(drugB)}
              className="font-bold text-slate-900 hover:text-sky-700 truncate"
            >
              {drugB?.brandName || selectedInteraction.drug2}
            </button>
          </div>

          {/* Quick Center Buttons */}
          <div className="grid grid-cols-2 gap-2 text-xs">
            {drugA && onCenterDrug && (
              <button
                onClick={() => onCenterDrug(drugA.id)}
                className="py-1.5 px-2.5 bg-sky-50 text-sky-700 border border-sky-200 rounded-lg font-semibold hover:bg-sky-100 transition-colors text-center truncate"
              >
                Center on {drugA.brandName}
              </button>
            )}
            {drugB && onCenterDrug && (
              <button
                onClick={() => onCenterDrug(drugB.id)}
                className="py-1.5 px-2.5 bg-sky-50 text-sky-700 border border-sky-200 rounded-lg font-semibold hover:bg-sky-100 transition-colors text-center truncate"
              >
                Center on {drugB.brandName}
              </button>
            )}
          </div>

          {/* Title & Description Card */}
          <div className={`p-4 rounded-xl border ${severityBg}`}>
            <h3 className="font-bold text-sm mb-1">{selectedInteraction.title}</h3>
            <p className="text-xs leading-relaxed opacity-95">
              {selectedInteraction.description}
            </p>
          </div>

          {/* Clinical Rationale */}
          <div>
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1">
              Pharmacological Mechanism
            </span>
            <div className="text-xs text-slate-700 bg-slate-50 p-3.5 rounded-xl border border-slate-200/80 leading-relaxed font-mono">
              {selectedInteraction.clinicalRationale}
            </div>
          </div>

          {/* Patient Actionable Advice */}
          <div>
            <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-1.5 mb-1.5">
              <Info className="w-3.5 h-3.5 text-sky-600" />
              Patient Usage Advice
            </span>
            <div className="text-xs text-sky-900 bg-sky-50/70 p-3.5 rounded-xl border border-sky-200/80 leading-relaxed font-medium">
              {selectedInteraction.patientActionableAdvice}
            </div>
          </div>
        </div>
      </aside>
    );
  }

  // Active Drug Card: Display selectedDrug or default to centerDrug
  const drug = selectedDrug || centerDrug || drugs[0];
  if (!drug) return null;

  const classItem = DRUG_CLASSES.find((c) => c.key === drug.classKey);
  const inCabinet = isInCabinet(drug.id);
  const isCurrentlyCentered = centerDrug?.id === drug.id;

  return (
    <aside
      aria-label="Medication Profile"
      className="w-80 md:w-96 bg-white border-l border-slate-200 h-full flex flex-col shadow-lg z-20 overflow-y-auto"
    >
      {/* Header */}
      <div className="p-4 border-b border-slate-100 flex items-start justify-between bg-slate-50/80">
        <div>
          <div className="flex items-center gap-2 text-xs text-slate-500 mb-1">
            <span
              className="w-2.5 h-2.5 rounded-full shrink-0"
              style={{ backgroundColor: classItem?.color || '#0284C7' }}
            />
            <span className="font-medium text-slate-700">{drug.category}</span>
            {isCurrentlyCentered && (
              <span className="px-1.5 py-0.5 rounded bg-sky-100 text-sky-800 text-[10px] font-bold">
                CENTER FOCUS
              </span>
            )}
          </div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            {drug.brandName}
          </h2>
          <div className="text-xs font-mono text-slate-500 mt-0.5">
            Active: {drug.genericName}
          </div>
        </div>
        {selectedDrug && (
          <button
            onClick={onClose}
            title="Reset focus to center medication"
            className="p-1 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200/50 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="p-5 space-y-4 flex-1">
        {/* Visual Thesaurus Re-center Action if not already center */}
        {!isCurrentlyCentered && onCenterDrug && (
          <button
            onClick={() => onCenterDrug(drug.id)}
            className="w-full py-2 px-3 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors shadow-xs"
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Re-Center Visual Thesaurus Web on {drug.brandName}</span>
          </button>
        )}

        {/* Cabinet Action Button */}
        <button
          onClick={() => onToggleCabinet(drug.id)}
          className={`w-full py-2.5 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 transition-all shadow-xs ${
            inCabinet
              ? 'bg-amber-50 text-amber-800 border border-amber-300 hover:bg-amber-100'
              : 'bg-slate-900 text-white hover:bg-slate-800'
          }`}
        >
          {inCabinet ? (
            <>
              <Check className="w-4 h-4 text-amber-600" />
              <span>Saved in "My Prescriptions"</span>
            </>
          ) : (
            <>
              <Plus className="w-4 h-4" />
              <span>Add to "My Prescriptions"</span>
            </>
          )}
        </button>

        {/* FDA Boxed Warning banner if applicable */}
        {drug.fdaBoxedWarning && (
          <div className="bg-rose-50 border border-rose-300 rounded-xl p-3.5 text-rose-900">
            <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-rose-800 mb-1">
              <ShieldAlert className="w-4 h-4 text-rose-600 shrink-0" />
              FDA Boxed Warning
            </div>
            <p className="text-xs leading-relaxed text-rose-950 font-medium">
              {drug.boxedWarningSummary || 'Carries a black box warning for serious adverse events.'}
            </p>
          </div>
        )}

        {/* Clinical Overview Description */}
        <div>
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            Clinical Overview
          </span>
          <p className="text-xs text-slate-600 leading-relaxed">
            {drug.description}
          </p>
        </div>

        {/* Common Side Effects */}
        <div>
          <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider block mb-2">
            Common Side Effects
          </span>
          <div className="flex flex-wrap gap-1.5">
            {drug.commonSideEffects.map((effect, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 text-xs bg-slate-100 text-slate-700 rounded-md font-medium"
              >
                {effect}
              </span>
            ))}
          </div>
        </div>

        {/* Patient Guidance Advice */}
        <div className="bg-sky-50/60 border border-sky-100 rounded-xl p-3.5">
          <span className="text-[11px] font-semibold text-sky-900 uppercase tracking-wider block mb-1 flex items-center gap-1">
            <Info className="w-3.5 h-3.5 text-sky-600" />
            Patient Usage Guidance
          </span>
          <p className="text-xs text-sky-950 leading-relaxed">
            {drug.patientAdvice}
          </p>
        </div>

        {/* Radiating Negative Interaction Spokes */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-3 h-3 text-sky-600" />
              Radiating Interaction Spokes ({getConflictCount(drug.id, interactions)})
            </span>
            <span className="text-[10px] text-slate-400">Click to re-center</span>
          </div>

          <div className="space-y-1.5 max-h-64 overflow-y-auto pr-1">
            {getConflictList(drug.id, onSelectDrug, onCenterDrug, onSelectInteraction, drugs, interactions, isInCabinet)}
          </div>
        </div>
      </div>
    </aside>
  );
};

// Helper for count
function getConflictCount(drugId: string, interactionList: DrugInteraction[] = INTERACTIONS): number {
  return interactionList.filter((i) => i.drug1 === drugId || i.drug2 === drugId).length;
}

// Helper for list of radiating spokes
function getConflictList(
  drugId: string,
  onSelectDrug: (d: Drug) => void,
  onCenterDrug: ((id: string) => void) | undefined,
  onSelectInteraction: (i: DrugInteraction) => void,
  drugList: Drug[] = DRUGS,
  interactionList: DrugInteraction[] = INTERACTIONS,
  isInCabinet: (id: string) => boolean
) {
  const matchingInteractions = interactionList.filter((i) => i.drug1 === drugId || i.drug2 === drugId);

  if (matchingInteractions.length === 0) {
    return (
      <div className="text-xs text-slate-400 italic py-2">
        No severe interactions logged for this medication in current dataset.
      </div>
    );
  }

  return matchingInteractions.map((inter) => {
    const otherId = inter.drug1 === drugId ? inter.drug2 : inter.drug1;
    const otherDrug = drugList.find((d) => d.id === otherId);
    if (!otherDrug) return null;

    const isSevere = inter.severity === 'severe';
    const isModerate = inter.severity === 'moderate';
    const inCab = isInCabinet(otherDrug.id);

    return (
      <div
        key={inter.id}
        className={`p-2.5 rounded-lg border transition-all flex items-center justify-between group ${
          inCab
            ? 'bg-rose-50/70 border-rose-200 hover:border-rose-300'
            : 'bg-white border-slate-200/90 hover:border-sky-300 hover:bg-slate-50'
        }`}
      >
        <div className="flex-1 min-w-0 mr-2">
          <div className="flex items-center gap-1.5">
            <span
              className={`w-2 h-2 rounded-full shrink-0 ${
                isSevere ? 'bg-rose-500' : isModerate ? 'bg-orange-500' : 'bg-amber-400'
              }`}
            />
            <button
              onClick={() => onCenterDrug ? onCenterDrug(otherDrug.id) : onSelectDrug(otherDrug)}
              title="Click to re-center Visual Thesaurus on this drug"
              className="text-xs font-bold text-slate-800 hover:text-sky-700 truncate text-left"
            >
              {otherDrug.brandName}
            </button>
            {inCab && (
              <span className="text-[9px] font-bold px-1 py-0.2 bg-rose-200 text-rose-800 rounded">
                Cabinet
              </span>
            )}
          </div>
          <div className="text-[11px] text-slate-500 truncate pl-3.5">
            {inter.title}
          </div>
        </div>

        <div className="flex items-center gap-1">
          {onCenterDrug && (
            <button
              onClick={() => onCenterDrug(otherDrug.id)}
              title="Re-center on this drug"
              className="p-1 text-slate-400 hover:text-sky-600 hover:bg-sky-50 rounded transition-colors text-[10px] font-semibold"
            >
              Center
            </button>
          )}
          <button
            onClick={() => onSelectInteraction(inter)}
            title="Inspect interaction details"
            className="p-1 text-slate-400 hover:text-sky-600 hover:bg-sky-50 rounded transition-colors shrink-0"
          >
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    );
  });
}
