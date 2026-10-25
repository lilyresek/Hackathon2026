import React, { useState } from 'react';
import { DRUGS, INTERACTIONS, getInteractionBetween, Drug, DrugInteraction } from '../data/drugData';
import {
  Search,
  ArrowRightLeft,
  AlertTriangle,
  CheckCircle2,
  Info,
  Compass,
  X,
  Sparkles
} from 'lucide-react';

interface InteractionCheckerProps {
  drugs?: Drug[];
  interactions?: DrugInteraction[];
  isOpen: boolean;
  onClose: () => void;
  onFocusInteractionOnGraph: (drugAId: string, drugBId: string) => void;
}

export const InteractionChecker: React.FC<InteractionCheckerProps> = ({
  drugs = DRUGS,
  interactions = INTERACTIONS,
  isOpen,
  onClose,
  onFocusInteractionOnGraph,
}) => {
  const [drugAId, setDrugAId] = useState<string>(drugs[0]?.id || 'warfarin');
  const [drugBId, setDrugBId] = useState<string>(drugs[1]?.id || 'aspirin');

  if (!isOpen) return null;

  const drugA = drugs.find((d) => d.id === drugAId);
  const drugB = drugs.find((d) => d.id === drugBId);

  const interaction = getInteractionBetween(drugAId, drugBId, interactions);


  const quickPairs: { label: string; a: string; b: string }[] = [
    { label: 'Warfarin + Aspirin', a: 'warfarin', b: 'aspirin' },
    { label: 'Nitrostat + Viagra', a: 'nitrostat', b: 'viagra' },
    { label: 'Zoloft + Tramadol', a: 'zoloft', b: 'tramadol' },
    { label: 'Lipitor + Diflucan', a: 'lipitor', b: 'diflucan' },
    { label: 'Lisinopril + Ibuprofen', a: 'lisinopril', b: 'ibuprofen' },
    { label: 'Metformin + Synthroid', a: 'metformin', b: 'synthroid' },
  ];

  const handleSwap = () => {
    const temp = drugAId;
    setDrugAId(drugBId);
    setDrugBId(temp);
  };

  const handleLocateOnGraph = () => {
    onClose();
    onFocusInteractionOnGraph(drugAId, drugBId);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl max-w-xl w-full border border-slate-200 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/80">
          <div>
            <h3 className="text-base font-bold text-slate-900">
              Interaction Query Tool
            </h3>
            <p className="text-xs text-slate-500">
              Select any two medications to check for documented clinical interactions.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-200/60 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Query Controls */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Dual Drug Selectors */}
          <div className="grid grid-cols-1 sm:grid-cols-[1fr_auto_1fr] items-center gap-3">
            {/* Drug A */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                Primary Drug
              </label>
              <select
                value={drugAId}
                onChange={(e) => setDrugAId(e.target.value)}
                className="w-full px-3 py-2 text-xs font-semibold text-slate-800 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              >
                {drugs.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.brandName} ({d.genericName})
                  </option>
                ))}
              </select>
            </div>

            {/* Swap Button */}
            <div className="flex sm:justify-center pt-2 sm:pt-4">
              <button
                onClick={handleSwap}
                title="Swap drugs"
                className="p-2 text-slate-400 hover:text-sky-600 hover:bg-sky-50 rounded-xl border border-slate-200 transition-colors"
              >
                <ArrowRightLeft className="w-4 h-4" />
              </button>
            </div>

            {/* Drug B */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                Secondary Drug
              </label>
              <select
                value={drugBId}
                onChange={(e) => setDrugBId(e.target.value)}
                className="w-full px-3 py-2 text-xs font-semibold text-slate-800 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              >
                {drugs.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.brandName} ({d.genericName})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Quick Test Pairs */}
          <div>
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              Common Test Combinations
            </span>
            <div className="flex flex-wrap gap-1.5">
              {quickPairs.map((p) => {
                const isSelected =
                  (drugAId === p.a && drugBId === p.b) || (drugAId === p.b && drugBId === p.a);
                return (
                  <button
                    key={p.label}
                    onClick={() => {
                      setDrugAId(p.a);
                      setDrugBId(p.b);
                    }}
                    className={`px-2.5 py-1 text-xs rounded-lg border transition-colors ${
                      isSelected
                        ? 'bg-sky-100 text-sky-800 border-sky-300 font-medium'
                        : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    {p.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Result Presentation */}
          <div className="pt-2 border-t border-slate-100">
            {drugAId === drugBId ? (
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center text-xs text-slate-500">
                Please select two distinct medications to check for pairwise interactions.
              </div>
            ) : interaction ? (
              <div
                className={`rounded-xl border p-4.5 space-y-3.5 ${
                  interaction.severity === 'severe'
                    ? 'bg-rose-50/70 border-rose-200'
                    : interaction.severity === 'moderate'
                    ? 'bg-orange-50/70 border-orange-200'
                    : 'bg-amber-50/70 border-amber-200'
                }`}
              >
                {/* Result Status Header */}
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider text-white ${
                        interaction.severity === 'severe'
                          ? 'bg-rose-600'
                          : interaction.severity === 'moderate'
                          ? 'bg-orange-500'
                          : 'bg-amber-500'
                      }`}
                    >
                      {interaction.severity} Risk
                    </span>
                    <span className="text-xs font-semibold text-slate-800 capitalize">
                      {interaction.mechanismType === 'metabolic'
                        ? 'Metabolic (CYP450)'
                        : interaction.mechanismType === 'clearance'
                        ? 'Renal Clearance'
                        : 'Synergistic Adverse Effect'}
                    </span>
                  </div>
                  <button
                    onClick={handleLocateOnGraph}
                    className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors shadow-2xs"
                  >
                    <Compass className="w-3.5 h-3.5 text-sky-600" />
                    <span>View on Web</span>
                  </button>
                </div>

                <h4 className="text-sm font-bold text-slate-900 leading-snug">
                  {interaction.title}
                </h4>

                <p className="text-xs text-slate-700 leading-relaxed font-medium">
                  {interaction.description}
                </p>

                <div className="bg-white/80 rounded-lg p-3 border border-slate-200/60 text-xs text-slate-600 space-y-1">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">
                    Clinical Mechanism
                  </span>
                  <p className="leading-relaxed">{interaction.clinicalRationale}</p>
                </div>

                <div className="bg-white/90 rounded-lg p-3 border border-sky-200 text-xs text-sky-950 font-medium">
                  <span className="text-[10px] uppercase font-bold text-sky-700 block mb-0.5">
                    Patient Directive
                  </span>
                  <p>{interaction.patientActionableAdvice}</p>
                </div>
              </div>
            ) : (
              <div className="p-5 rounded-xl bg-emerald-50/70 border border-emerald-200 text-emerald-950 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-800 uppercase tracking-wider">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  No Direct Interaction Documented
                </div>
                <p className="text-xs text-emerald-900 leading-relaxed">
                  No major adverse interaction between <strong>{drugA?.brandName}</strong> and{' '}
                  <strong>{drugB?.brandName}</strong> is logged in this database.
                </p>
                <div className="text-[11px] text-emerald-800/80 pt-1 border-t border-emerald-200/60">
                  Note: Always consult your physician or pharmacist regarding dosage intervals and over-the-counter supplements.
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-200/60 rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
