export interface Drug {
  id: string;
  brandName: string;
  genericName: string;
  category: string;
  classKey: 'nsaid' | 'anticoagulant' | 'cardiovascular' | 'psychiatric' | 'stimulant' | 'sedative' | 'analgesic' | 'antimicrobial' | 'metabolic' | 'supplement';
  description: string;
  commonSideEffects: string[];
  patientAdvice: string;
  fdaBoxedWarning?: boolean;
  boxedWarningSummary?: string;
  color?: string;
  isHub?: boolean;
  degree?: number;
}


export interface DrugInteraction {
  id: string;
  drug1: string;
  drug2: string;
  severity: 'severe' | 'moderate' | 'minor';
  mechanismType: 'synergistic' | 'metabolic' | 'clearance';
  title: string;
  description: string;
  clinicalRationale: string;
  patientActionableAdvice: string;
}

export const DRUG_CLASSES: { key: Drug['classKey']; label: string; color: string; bgLight: string }[] = [
  { key: 'nsaid', label: 'NSAID / Anti-inflammatory', color: '#0284C7', bgLight: '#E0F2FE' },
  { key: 'anticoagulant', label: 'Blood Thinners & Anticoagulants', color: '#E11D48', bgLight: '#FFE4E6' },
  { key: 'cardiovascular', label: 'Cardiovascular & Blood Pressure', color: '#2563EB', bgLight: '#DBEAFE' },
  { key: 'psychiatric', label: 'Antidepressants & SSRIs', color: '#7C3AED', bgLight: '#EDE9FE' },
  { key: 'stimulant', label: 'CNS Stimulants & ADHD', color: '#D97706', bgLight: '#FEF3C7' },
  { key: 'sedative', label: 'Sedatives & Sleep Aids', color: '#475569', bgLight: '#F1F5F9' },
  { key: 'analgesic', label: 'Analgesics & Pain Relievers', color: '#0D9488', bgLight: '#CCFBF1' },
  { key: 'antimicrobial', label: 'Antibiotics & Antifungals', color: '#059669', bgLight: '#D1FAE5' },
  { key: 'metabolic', label: 'Metabolic & Endocrine', color: '#4F46E5', bgLight: '#EEF2FF' },
  { key: 'supplement', label: 'Herbal & Dietary Supplements', color: '#65A30D', bgLight: '#ECFCCB' },
];

export const RAW_DRUGS: Drug[] = [
  {
    id: 'aspirin',
    brandName: 'Aspirin',
    genericName: 'Acetylsalicylic Acid',
    category: 'NSAID & Antiplatelet',
    classKey: 'nsaid',
    description: 'Over-the-counter pain reliever, fever reducer, and low-dose cardiovascular antiplatelet agent.',
    commonSideEffects: ['Upset stomach', 'Heartburn', 'Easy bruising', 'Bleeding gums', 'Mild headache'],
    patientAdvice: 'Take with food or a full glass of water to reduce stomach irritation. Avoid excessive alcohol.',
    fdaBoxedWarning: false,
  },
  {
    id: 'ibuprofen',
    brandName: 'Ibuprofen',
    genericName: 'Ibuprofen (Advil, Motrin)',
    category: 'Nonsteroidal Anti-inflammatory (NSAID)',
    classKey: 'nsaid',
    description: 'Widely used pain reliever and anti-inflammatory for muscle aches, arthritis, and fever.',
    commonSideEffects: ['Nausea', 'Gastric distress', 'Dizziness', 'Fluid retention', 'Elevated blood pressure'],
    patientAdvice: 'Always take with food or milk. Avoid taking multiple NSAID products concurrently.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Increased risk of serious cardiovascular thrombotic events and gastrointestinal ulceration/bleeding.',
  },
  {
    id: 'warfarin',
    brandName: 'Warfarin',
    genericName: 'Warfarin Sodium (Coumadin)',
    category: 'Vitamin K Antagonist Anticoagulant',
    classKey: 'anticoagulant',
    description: 'Potent prescription blood thinner used to prevent deep vein thrombosis, pulmonary embolism, and stroke in atrial fibrillation.',
    commonSideEffects: ['Bruising easily', 'Prolonged bleeding from cuts', 'Nosebleeds', 'Heavy menstrual flow', 'Skin necrosis (rare)'],
    patientAdvice: 'Requires regular INR blood monitoring. Maintain consistent dietary intake of Vitamin K (green leafy vegetables).',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Can cause major or fatal bleeding. Regular monitoring of PT/INR is mandatory.',
  },
  {
    id: 'plavix',
    brandName: 'Plavix',
    genericName: 'Clopidogrel Bisulfate',
    category: 'P2Y12 Platelet Inhibitor',
    classKey: 'anticoagulant',
    description: 'Antiplatelet medication used to prevent heart attack and stroke in patients with coronary stent placement or peripheral vascular disease.',
    commonSideEffects: ['Bruising', 'Minor bleeding', 'Diarrhea', 'Rash', 'Abdominal discomfort'],
    patientAdvice: 'Do not stop abruptly without consulting your cardiologist. Inform dentists and surgeons prior to procedures.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Diminished antiplatelet effect in patients who are CYP2C19 poor metabolizers.',
  },
  {
    id: 'eliquis',
    brandName: 'Eliquis',
    genericName: 'Apixaban',
    category: 'Direct Factor Xa Inhibitor (DOAC)',
    classKey: 'anticoagulant',
    description: 'Modern direct oral anticoagulant that inhibits Factor Xa to prevent blood clots without regular INR lab tests.',
    commonSideEffects: ['Nausea', 'Minor bruising', 'Gingival bleeding', 'Anemia', 'Fatigue'],
    patientAdvice: 'Take twice daily exactly 12 hours apart. Do not skip doses due to short half-life.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Premature discontinuation increases risk of thrombotic events; risk of spinal/epidural hematoma.',
  },
  {
    id: 'lipitor',
    brandName: 'Lipitor',
    genericName: 'Atorvastatin Calcium',
    category: 'HMG-CoA Reductase Inhibitor (Statin)',
    classKey: 'cardiovascular',
    description: 'Cholesterol-lowering medication used to reduce cardiovascular morbidity and LDL cholesterol.',
    commonSideEffects: ['Muscle aches (myalgia)', 'Joint discomfort', 'Diarrhea', 'Mild liver enzyme elevation', 'Digestive issues'],
    patientAdvice: 'Can be taken with or without food at any time of day. Report unexplained muscle soreness or dark urine immediately.',
    fdaBoxedWarning: false,
  },
  {
    id: 'lisinopril',
    brandName: 'Lisinopril',
    genericName: 'Lisinopril (Prinivil, Zestril)',
    category: 'ACE Inhibitor Antihypertensive',
    classKey: 'cardiovascular',
    description: 'High blood pressure medication and heart failure therapy that relaxes blood vessels by blocking angiotensin II.',
    commonSideEffects: ['Dry persistent cough', 'Dizziness on standing', 'Headache', 'Elevated potassium', 'Fatigue'],
    patientAdvice: 'Avoid salt substitutes containing potassium. Rise slowly from sitting to minimize orthostatic lightheadedness.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Can cause fetal harm or death when administered during pregnancy.',
  },
  {
    id: 'nitrostat',
    brandName: 'Nitrostat',
    genericName: 'Nitroglycerin Sublingual',
    category: 'Nitrate Vasodilator',
    classKey: 'cardiovascular',
    description: 'Fast-acting sublingual vasodilator used to relieve acute chest pain (angina pectoris) during ischemic episodes.',
    commonSideEffects: ['Throbbing headache', 'Sudden dizziness', 'Facial flushing', 'Low blood pressure', 'Rapid pulse'],
    patientAdvice: 'Sit down before taking a dose. Place tablet under tongue; do not chew or swallow. Call 911 if pain persists after 5 minutes.',
    fdaBoxedWarning: false,
  },
  {
    id: 'zoloft',
    brandName: 'Zoloft',
    genericName: 'Sertraline Hydrochloride',
    category: 'Selective Serotonin Reuptake Inhibitor (SSRI)',
    classKey: 'psychiatric',
    description: 'Prescription antidepressant for major depressive disorder, generalized anxiety, panic attacks, and OCD.',
    commonSideEffects: ['Nausea', 'Insomnia', 'Tremors', 'Sexual dysfunction', 'Dry mouth', 'Diarrhea'],
    patientAdvice: 'May take 4 to 6 weeks for full therapeutic efficacy. Do not discontinue abruptly to prevent withdrawal syndrome.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Increased risk of suicidal thoughts and behaviors in children, adolescents, and young adults.',
  },
  {
    id: 'prozac',
    brandName: 'Prozac',
    genericName: 'Fluoxetine Hydrochloride',
    category: 'SSRI & CYP2D6 Inhibitor',
    classKey: 'psychiatric',
    description: 'Long-acting SSRI used for clinical depression, bulimia nervosa, and panic disorder with potent CYP enzyme interactions.',
    commonSideEffects: ['Sleep disturbances', 'Anorexia/weight loss', 'Nervousness', 'Headache', 'Drowsiness'],
    patientAdvice: 'Long elimination half-life; stays in system for weeks after last dose. Take early in the day if causing wakefulness.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Antidepressants increased the risk of suicidal thinking in young adults.',
  },
  {
    id: 'lexapro',
    brandName: 'Lexapro',
    genericName: 'Escitalopram Oxalate',
    category: 'Selective Serotonin Reuptake Inhibitor (SSRI)',
    classKey: 'psychiatric',
    description: 'Highly selective SSRI prescribed for depression and generalized anxiety disorder.',
    commonSideEffects: ['Fatigue', 'Excessive sweating', 'Decreased libido', 'Nausea', 'Somnolence'],
    patientAdvice: 'Take consistently at the same time each day. Consult physician before taking any cough or pain medicines.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Suicidality risk in adolescents and young adults under 25.',
  },
  {
    id: 'adderall',
    brandName: 'Adderall',
    genericName: 'Dextroamphetamine / Amphetamine',
    category: 'Central Nervous System Stimulant',
    classKey: 'stimulant',
    description: 'Controlled stimulant medication that enhances dopamine and norepinephrine transmission for ADHD and narcolepsy.',
    commonSideEffects: ['Loss of appetite', 'Insomnia', 'Increased heart rate', 'Dry mouth', 'Anxiety / Restlessness'],
    patientAdvice: 'Take early in the morning to prevent sleeplessness. Schedule II medication; store safely in a secure place.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'High potential for abuse and dependence. Risk of sudden cardiovascular death in structural heart defects.',
  },
  {
    id: 'vyvanse',
    brandName: 'Vyvanse',
    genericName: 'Lisdexamfetamine Dimesylate',
    category: 'Amphetamine Prodrug Stimulant',
    classKey: 'stimulant',
    description: 'Long-acting prodrug stimulant converted in blood cells to active dextroamphetamine for ADHD and binge eating disorder.',
    commonSideEffects: ['Decreased appetite', 'Insomnia', 'Irritability', 'Dry mouth', 'Tachycardia'],
    patientAdvice: 'Take once daily in the morning with or without food. Avoid caffeine which may compound heart palpitations.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'High potential for abuse and severe dependence.',
  },
  {
    id: 'xanax',
    brandName: 'Xanax',
    genericName: 'Alprazolam',
    category: 'Benzodiazepine Anxiolytic',
    classKey: 'sedative',
    description: 'Short-acting benzodiazepine that enhances GABA activity for acute anxiety and panic disorders.',
    commonSideEffects: ['Drowsiness', 'Lightheadedness', 'Impaired coordination', 'Memory fog', 'Slurred speech'],
    patientAdvice: 'Strictly avoid alcohol. Never drive or operate machinery while taking. Physical dependence can develop within weeks.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Concomitant use with opioids may result in profound sedation, respiratory depression, coma, and death.',
  },
  {
    id: 'valium',
    brandName: 'Valium',
    genericName: 'Diazepam',
    category: 'Long-acting Benzodiazepine',
    classKey: 'sedative',
    description: 'Long-acting benzodiazepine used for severe anxiety, muscle spasms, alcohol withdrawal, and seizure control.',
    commonSideEffects: ['Prolonged sedation', 'Muscle weakness', 'Ataxia', 'Confusion in elderly', 'Slowed reflexes'],
    patientAdvice: 'Long-acting metabolites accumulate over several days. Taper gradually under clinical guidance.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Risk of profound sedation, respiratory arrest, and fatality when combined with other CNS depressants.',
  },
  {
    id: 'ambien',
    brandName: 'Ambien',
    genericName: 'Zolpidem Tartrate',
    category: 'Non-Benzodiazepine Hypnotic (Z-Drug)',
    classKey: 'sedative',
    description: 'Sedative-hypnotic indicated for short-term treatment of sleep onset insomnia.',
    commonSideEffects: ['Morning grogginess', 'Dizziness', 'Complex sleep behaviors (sleepwalking)', 'Amnesia', 'Headache'],
    patientAdvice: 'Take immediately before getting into bed with at least 7-8 hours remaining before planned awakening.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Complex sleep behaviors including sleep-driving, sleep-cooking, and making calls while not fully awake.',
  },
  {
    id: 'tylenol',
    brandName: 'Tylenol',
    genericName: 'Acetaminophen (Paracetamol)',
    category: 'Analgesic & Antipyretic',
    classKey: 'analgesic',
    description: 'Ubiquitous non-opioid pain reliever and fever reducer that does not inhibit peripheral prostaglandins or cause stomach ulcers.',
    commonSideEffects: ['Nausea (mild)', 'Allergic skin reaction (rare)', 'Transient liver enzyme changes'],
    patientAdvice: 'Do not exceed 3,000 mg to 4,000 mg per 24 hours across all combined products to prevent liver toxicity.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Severe liver damage may occur if exceeding maximum daily doses or consuming alongside 3+ alcoholic drinks.',
  },
  {
    id: 'tramadol',
    brandName: 'Tramadol',
    genericName: 'Tramadol Hydrochloride (Ultram)',
    category: 'Synthetic Opioid & SNRI',
    classKey: 'analgesic',
    description: 'Dual-action analgesic acting as a mu-opioid receptor agonist and weak serotonin/norepinephrine reuptake inhibitor.',
    commonSideEffects: ['Constipation', 'Nausea', 'Dizziness', 'Drowsiness', 'Sweating', 'Pruritus'],
    patientAdvice: 'Risk of seizures and serotonin syndrome. Avoid alcohol and other sedating medications.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Addiction, abuse, misuse, life-threatening respiratory depression, and neonatal opioid withdrawal.',
  },
  {
    id: 'cipro',
    brandName: 'Cipro',
    genericName: 'Ciprofloxacin',
    category: 'Fluoroquinolone Antibiotic',
    classKey: 'antimicrobial',
    description: 'Broad-spectrum fluoroquinolone antibiotic targeting severe bacterial infections and strong CYP1A2 inhibitor.',
    commonSideEffects: ['Nausea', 'Diarrhea', 'Photosensitivity (sunburn)', 'Headache', 'Abdominal cramps'],
    patientAdvice: 'Do not take with antacids, calcium supplements, or milk. Protect skin from prolonged sunlight exposure.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Tendonitis, tendon rupture, peripheral neuropathy, and central nervous system toxicities.',
  },
  {
    id: 'diflucan',
    brandName: 'Diflucan',
    genericName: 'Fluconazole',
    category: 'Azole Antifungal & CYP Inhibitor',
    classKey: 'antimicrobial',
    description: 'Systemic antifungal agent used for candidiasis and fungal infections; potent inhibitor of CYP2C9 and CYP3A4 enzymes.',
    commonSideEffects: ['Headache', 'Nausea', 'Abdominal pain', 'Transient taste alteration', 'Mild rash'],
    patientAdvice: 'Can be taken with or without food. Tell your doctor about every medication you take before starting.',
    fdaBoxedWarning: false,
  },
  {
    id: 'metformin',
    brandName: 'Metformin',
    genericName: 'Metformin Hydrochloride (Glucophage)',
    category: 'Biguanide Antidiabetic',
    classKey: 'metabolic',
    description: 'First-line oral antidiabetic drug that reduces hepatic glucose production and enhances peripheral insulin sensitivity.',
    commonSideEffects: ['Diarrhea', 'Flatulence', 'Abdominal bloating', 'Metallic taste', 'Vitamin B12 deficiency'],
    patientAdvice: 'Take with evening meals to minimize GI side effects. Temporarily withhold prior to iodinated radiocontrast procedures.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Rare but potentially fatal lactic acidosis, particularly in patients with renal impairment.',
  },
  {
    id: 'synthroid',
    brandName: 'Synthroid',
    genericName: 'Levothyroxine Sodium',
    category: 'Thyroid Hormone Replacement',
    classKey: 'metabolic',
    description: 'Synthetic T4 hormone prescribed to restore normal thyroid levels in hypothyroidism.',
    commonSideEffects: ['Palpitations (if overdosed)', 'Heat intolerance', 'Weight loss', 'Nervousness', 'Tremors'],
    patientAdvice: 'Take first thing in the morning on an empty stomach with a full glass of water, 30-60 minutes before breakfast.',
    fdaBoxedWarning: true,
    boxedWarningSummary: 'Should not be used for the treatment of obesity or for weight loss.',
  },
  {
    id: 'viagra',
    brandName: 'Viagra',
    genericName: 'Sildenafil Citrate',
    category: 'Phosphodiesterase-5 (PDE5) Inhibitor',
    classKey: 'cardiovascular',
    description: 'PDE5 inhibitor that promotes cyclic GMP accumulation to facilitate penile arterial vasodilation and pulmonary hypertension relief.',
    commonSideEffects: ['Facial flushing', 'Headache', 'Nasal congestion', 'Visual blue tinge', 'Dyspepsia'],
    patientAdvice: 'Take approximately 30-60 minutes prior to anticipated activity. Absolute contraindication with nitrates.',
    fdaBoxedWarning: false,
  },
  {
    id: 'st-johns-wort',
    brandName: "St. John's Wort",
    genericName: 'Hypericum perforatum Extract',
    category: 'Herbal Supplement & CYP3A4 / P-gp Inducer',
    classKey: 'supplement',
    description: 'Popular over-the-counter herbal botanical taken for mild depression; notorious for triggering dangerous pharmacologic interactions.',
    commonSideEffects: ['Photosensitivity', 'Dry mouth', 'Mild gastrointestinal upset', 'Dizziness', 'Restlessness'],
    patientAdvice: 'Always inform your pharmacist or healthcare team before starting any herbal product.',
    fdaBoxedWarning: false,
  },
];

export const INTERACTIONS: DrugInteraction[] = [
  // SEVERE INTERACTIONS
  {
    id: 'warfarin-aspirin',
    drug1: 'warfarin',
    drug2: 'aspirin',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Severe Hemorrhage & Gastrointestinal Bleeding',
    description: 'Combining a potent anticoagulant with an antiplatelet creates severe additive bleeding risk throughout the body.',
    clinicalRationale: 'Aspirin permanently blocks platelet thromboxane A2 while Warfarin inhibits hepatic synthesis of coagulation factors II, VII, IX, and X. Combined use disables both primary and secondary hemostasis, dramatically raising intracranial and gastrointestinal bleed risk.',
    patientActionableAdvice: 'Avoid taking Aspirin or over-the-counter pain compounds while on Warfarin unless specifically prescribed and monitored by your cardiologist.',
  },
  {
    id: 'warfarin-ibuprofen',
    drug1: 'warfarin',
    drug2: 'ibuprofen',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Gastrointestinal Ulceration & Massive Bleeding Risk',
    description: 'NSAIDs irritate the stomach lining and disrupt platelet function, which can trigger massive bleeding when combined with Warfarin.',
    clinicalRationale: 'Ibuprofen causes gastric mucosal injury and reversible platelet inhibition. In anticoagulated patients, minor mucosal erosions rapidly progress to major hemorrhage.',
    patientActionableAdvice: 'Do not take Ibuprofen with Warfarin. Use Acetaminophen (at modest doses) for minor aches after checking with your doctor.',
  },
  {
    id: 'warfarin-diflucan',
    drug1: 'warfarin',
    drug2: 'diflucan',
    severity: 'severe',
    mechanismType: 'metabolic',
    title: 'Potent CYP2C9 Inhibition Causing Critical INR Spikes',
    description: 'Fluconazole blocks the liver enzyme that breaks down Warfarin, causing blood levels of Warfarin to surge uncontrollably.',
    clinicalRationale: 'Fluconazole is a potent inhibitor of cytochrome P450 2C9, the primary metabolic clearance pathway for the potent S-enantiomer of warfarin. Co-administration commonly doubles or triples the patient’s INR within 48 to 72 hours.',
    patientActionableAdvice: 'Urgent medical attention required. Your doctor must drastically reduce the Warfarin dose (often by 50%) and perform serial INR blood draws.',
  },
  {
    id: 'zoloft-tramadol',
    drug1: 'zoloft',
    drug2: 'tramadol',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Life-Threatening Serotonin Syndrome & Seizure Risk',
    description: 'Both medications raise serotonin levels in the brain, which can cause fever, rigid muscles, rapid pulse, delirium, and seizures.',
    clinicalRationale: 'Sertraline blocks serotonin reuptake while Tramadol blocks serotonin reuptake and stimulates release. The dual serotonergic load can trigger fulminant Serotonin Syndrome (hyperthermia, clonus, autonomic instability) and lowers seizure threshold.',
    patientActionableAdvice: 'Do not combine without close medical supervision. Seek emergency care immediately if experiencing tremors, high fever, agitation, or sweating.',
  },
  {
    id: 'prozac-tramadol',
    drug1: 'prozac',
    drug2: 'tramadol',
    severity: 'severe',
    mechanismType: 'metabolic',
    title: 'Metabolic Blockade & Toxic Serotonin Accumulation',
    description: 'Prozac shuts down the enzyme that breaks down Tramadol and adds serotonin stimulation, multiplying toxic risks.',
    clinicalRationale: 'Fluoxetine strongly inhibits CYP2D6, suppressing conversion of tramadol to its active M1 metabolite, resulting in tramadol accumulation and dual serotonin toxicity.',
    patientActionableAdvice: 'Seek alternative pain medications. Never take Tramadol with Prozac without explicit pain specialist and psychiatric consultation.',
  },
  {
    id: 'xanax-ambien',
    drug1: 'xanax',
    drug2: 'ambien',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Severe Central Nervous System & Respiratory Depression',
    description: 'Combining two potent sedatives can cause extreme confusion, memory loss, respiratory arrest, coma, and accidental death.',
    clinicalRationale: 'Both alprazolam and zolpidem act on the GABA-A receptor complex, producing additive central nervous system depression, profound sedation, severe psychomotor impairment, and respiratory failure.',
    patientActionableAdvice: 'Never take Xanax and Ambien together. If sleep is impaired, consult your prescribing physician for safe single-agent sleep hygiene options.',
  },
  {
    id: 'valium-tramadol',
    drug1: 'valium',
    drug2: 'tramadol',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Concurrent Opioid & Benzodiazepine Respiratory Arrest',
    description: 'Mixing opioids with benzodiazepines is flagged by the FDA as one of the highest causes of fatal respiratory collapse.',
    clinicalRationale: 'Concomitant administration of opioids and benzodiazepines exerts synergistic depressant actions on brainstem respiratory centers, blunting hypercapnic and hypoxic ventilatory drive.',
    patientActionableAdvice: 'FDA Boxed Warning. Ensure naloxone (Narcan) is readily accessible in your household. Never exceed prescribed doses.',
  },
  {
    id: 'nitrostat-viagra',
    drug1: 'nitrostat',
    drug2: 'viagra',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Catastrophic, Potentially Fatal Blood Pressure Collapse',
    description: 'Absolute contraindication: taking Nitroglycerin with Viagra can drop blood pressure to zero, causing shock or fatal cardiac arrest.',
    clinicalRationale: 'Nitroglycerin generates nitric oxide, which stimulates guanylate cyclase to synthesize cGMP. Sildenafil prevents cGMP degradation by inhibiting PDE5. The unchecked cGMP accumulation induces massive systemic vasodilation and refractory shock.',
    patientActionableAdvice: 'ABSOLUTE CONTRAINDICATION. Never take Nitroglycerin within 24 to 48 hours of taking Viagra or similar PDE5 inhibitors under any circumstances.',
  },
  {
    id: 'lipitor-diflucan',
    drug1: 'lipitor',
    drug2: 'diflucan',
    severity: 'severe',
    mechanismType: 'metabolic',
    title: 'CYP3A4 Inhibition Causing Severe Rhabdomyolysis',
    description: 'Fluconazole blocks statin clearance, allowing toxic levels of Lipitor to build up, destroying muscle tissue and damaging kidneys.',
    clinicalRationale: 'Atorvastatin is extensively metabolized by hepatic CYP3A4. Fluconazole inhibits this pathway, multiplying plasma statin concentrations by up to 300%, triggering massive myopathy and acute renal tubular necrosis.',
    patientActionableAdvice: 'Temporarily pause Lipitor while taking a course of Diflucan if instructed by your physician. Report tea-colored urine or severe calf/shoulder pain.',
  },
  {
    id: 'st-johns-wort-zoloft',
    drug1: 'st-johns-wort',
    drug2: 'zoloft',
    severity: 'severe',
    mechanismType: 'synergistic',
    title: 'Herbal Supplement Induced Serotonin Syndrome',
    description: "Patients often assume St. John's Wort is harmless because it is natural, but combining it with Zoloft causes toxic serotonin overload.",
    clinicalRationale: 'Hyperforin and hypericin in St. John\'s Wort inhibit synaptic reuptake of serotonin, dopamine, and norepinephrine, synergizing directly with sertraline to provoke hyperpyrexia, shivering, and autonomic crisis.',
    patientActionableAdvice: "Discontinue St. John's Wort immediately if prescribed an antidepressant. Always disclose all dietary supplements to your pharmacist.",
  },
  {
    id: 'st-johns-wort-warfarin',
    drug1: 'st-johns-wort',
    drug2: 'warfarin',
    severity: 'severe',
    mechanismType: 'metabolic',
    title: 'CYP2C9 Induction Leading to Clot Formation & Stroke',
    description: "St. John's Wort accelerates the breakdown of Warfarin, causing blood to become too thick and drastically increasing blood clot and stroke risk.",
    clinicalRationale: 'St. John\'s Wort is a strong inducer of hepatic CYP2C9, CYP3A4, and intestinal P-glycoprotein through the PXR receptor, dropping warfarin serum concentrations and rendering anticoagulation subtherapeutic.',
    patientActionableAdvice: "Do not take St. John's Wort with Warfarin. Sudden cessation or initiation of the herb causes wild, dangerous swings in your INR numbers.",
  },
  {
    id: 'cipro-warfarin',
    drug1: 'cipro',
    drug2: 'warfarin',
    severity: 'severe',
    mechanismType: 'metabolic',
    title: 'Gut Flora Depletion & Metabolic Interference Raising Bleed Risk',
    description: 'Cipro wipes out Vitamin K producing bacteria in your intestines and slows Warfarin clearance, leading to unexpected severe bleeding.',
    clinicalRationale: 'Ciprofloxacin disrupts intestinal microflora that synthesize Vitamin K2 while weakly inhibiting CYP1A2/CYP3A4. The resulting Vitamin K depletion enhances warfarin sensitivity, causing sudden INR elevation.',
    patientActionableAdvice: 'Check INR within 3 days of starting Cipro. Watch closely for nosebleeds, dark urine, or unusual bruising.',
  },

  // MODERATE INTERACTIONS
  {
    id: 'adderall-zoloft',
    drug1: 'adderall',
    drug2: 'zoloft',
    severity: 'moderate',
    mechanismType: 'synergistic',
    title: 'Additive Cardiovascular Stimulation & Mild Serotonin Excess',
    description: 'Combining stimulants with SSRIs can increase heart palpitations, spike blood pressure, and cause anxiety or tremors.',
    clinicalRationale: 'Amphetamines promote catecholamine and mild serotonin release, while sertraline blocks serotonin reuptake. Co-administration increases sympathetic tone (tachycardia, hypertension) and requires monitoring for emergent agitation.',
    patientActionableAdvice: 'Monitor blood pressure and resting pulse regularly. Report chest pounding, acute restlessness, or insomnia to your physician.',
  },
  {
    id: 'adderall-prozac',
    drug1: 'adderall',
    drug2: 'prozac',
    severity: 'moderate',
    mechanismType: 'metabolic',
    title: 'Enzyme Competition Elevating Stimulant Exposure',
    description: 'Prozac inhibits CYP2D6, which processes Adderall, leading to stronger and longer-lasting stimulant effects and jitters.',
    clinicalRationale: 'Fluoxetine and its active metabolite norfluoxetine are potent CYP2D6 inhibitors. Because dextroamphetamine is partially metabolized by CYP2D6, blood levels can climb, magnifying cardiovascular and central stimulation.',
    patientActionableAdvice: 'Your doctor may prescribe a lower stimulant starting dose. Limit intake of coffee, tea, and energy beverages.',
  },
  {
    id: 'lisinopril-ibuprofen',
    drug1: 'lisinopril',
    drug2: 'ibuprofen',
    severity: 'moderate',
    mechanismType: 'clearance',
    title: 'Blunted Blood Pressure Control & Acute Kidney Strain',
    description: 'Regular NSAID pain relievers counteract Lisinopril, causing blood pressure to rise and placing strain on kidney filtration.',
    clinicalRationale: 'NSAIDs suppress renal vasodilatory prostaglandins (PGE2/PGI2), producing afferent arteriolar vasoconstriction while Lisinopril produces efferent arteriolar vasodilation. This "triple whammy" hemodynamic mismatch decreases glomerular filtration rate (GFR).',
    patientActionableAdvice: 'Avoid chronic NSAID use while taking blood pressure medicine. For occasional mild pain, ask your doctor if Acetaminophen is appropriate.',
  },
  {
    id: 'plavix-aspirin',
    drug1: 'plavix',
    drug2: 'aspirin',
    severity: 'moderate',
    mechanismType: 'synergistic',
    title: 'Dual Antiplatelet Therapy (DAPT) Bleeding Precaution',
    description: 'Often prescribed together deliberately after stents, but requires strict vigilance due to cumulative hemorrhagic danger.',
    clinicalRationale: 'Concurrent blockade of platelet activation via COX-1 inhibition (aspirin) and P2Y12 adenosine diphosphate antagonism (clopidogrel) provides potent antithrombotic defense but doubles major bleed frequency.',
    patientActionableAdvice: 'Take only under strict cardiological protocol. Never add extra over-the-counter NSAIDs like Advil or Aleve.',
  },
  {
    id: 'eliquis-ibuprofen',
    drug1: 'eliquis',
    drug2: 'ibuprofen',
    severity: 'moderate',
    mechanismType: 'synergistic',
    title: 'Elevated Internal Bleeding & Mucosal Breakdown',
    description: 'Taking Advil or Motrin with Eliquis raises internal bleeding risk because both interfere with the body’s clotting mechanisms.',
    clinicalRationale: 'Direct Factor Xa inhibition combined with NSAID-induced platelet impairment and gastric mucosa damage elevates clinical bleeding incidence by up to three-fold.',
    patientActionableAdvice: 'Avoid all NSAIDs while on Eliquis. If dealing with chronic pain, consult your physician for topical or non-NSAID alternatives.',
  },
  {
    id: 'xanax-zoloft',
    drug1: 'xanax',
    drug2: 'zoloft',
    severity: 'moderate',
    mechanismType: 'metabolic',
    title: 'Mild CYP3A4 Competition Increasing Drowsiness',
    description: 'Zoloft can slightly reduce the breakdown of Xanax, leading to prolonged daytime sleepiness and slowed reaction time.',
    clinicalRationale: 'Sertraline exerts modest inhibitory effects on CYP3A4, which is responsible for alprazolam clearance, mildly increasing alprazolam peak concentration and half-life.',
    patientActionableAdvice: 'Pay attention to coordination and alertness. Do not drive if feeling fatigued or lightheaded.',
  },
  {
    id: 'warfarin-tylenol',
    drug1: 'warfarin',
    drug2: 'tylenol',
    severity: 'moderate',
    mechanismType: 'metabolic',
    title: 'Prolonged High-Dose Acetaminophen Boosting Anticoagulation',
    description: 'While safer than NSAIDs, taking high doses of Tylenol for more than a few days can unexpectedly elevate INR and bleed risk.',
    clinicalRationale: 'The toxic metabolite of acetaminophen (NAPQI) is thought to inhibit Vitamin K oxide reductase and depletes hepatic glutathione, enhancing the hypoprothrombinemic response to warfarin.',
    patientActionableAdvice: 'Occasional single doses (under 1,000 mg) are generally fine, but if taking Tylenol regularly for more than 3-4 days, notify your anticoagulation clinic.',
  },
  {
    id: 'metformin-lisinopril',
    drug1: 'metformin',
    drug2: 'lisinopril',
    severity: 'minor',
    mechanismType: 'clearance',
    title: 'Renal Function Monitoring Precaution',
    description: 'Both medications rely on healthy kidneys; severe dehydration or renal decline requires prompt medical assessment.',
    clinicalRationale: 'Lisinopril can alter renal perfusion in volume-depleted states, while Metformin clearance is dependent on tubular excretion. If renal impairment develops, risk of metformin accumulation and lactic acidosis increases.',
    patientActionableAdvice: 'Stay adequately hydrated, especially in hot weather or during stomach illnesses. Ensure routine annual kidney lab checks.',
  },
  {
    id: 'lexapro-aspirin',
    drug1: 'lexapro',
    drug2: 'aspirin',
    severity: 'moderate',
    mechanismType: 'synergistic',
    title: 'Platelet Serotonin Depletion Bleeding Risk',
    description: 'SSRIs deplete serotonin in blood platelets, which impairs clotting and enhances Aspirin’s blood-thinning effect.',
    clinicalRationale: 'Platelets require serotonin uptake from plasma for dense granule aggregation. SSRIs deplete platelet serotonin stores; when combined with aspirin, the risk of upper GI bleeding increases 3 to 5 times.',
    patientActionableAdvice: 'Watch for frequent nosebleeds or blood in stool. A stomach-protecting medication (PPI) is sometimes recommended by doctors.',
  },
  {
    id: 'st-johns-wort-lipitor',
    drug1: 'st-johns-wort',
    drug2: 'lipitor',
    severity: 'moderate',
    mechanismType: 'metabolic',
    title: 'Accelerated Statin Clearance Reducing Cholesterol Control',
    description: "St. John's Wort speeds up the elimination of Lipitor, causing cholesterol levels to climb back to dangerous ranges.",
    clinicalRationale: 'St. John\'s Wort induces CYP3A4, reducing atorvastatin area-under-the-curve (AUC) by up to 50%, resulting in loss of cardiovascular protection.',
    patientActionableAdvice: "Do not take St. John's Wort without consulting your doctor; you may lose the preventative benefits of your statin.",
  },
  {
    id: 'synthroid-calcium-iron',
    drug1: 'synthroid',
    drug2: 'aspirin',
    severity: 'minor',
    mechanismType: 'clearance',
    title: 'High-Dose Salicylate Protein Binding Displacement',
    description: 'High doses of aspirin can temporarily displace thyroid hormone from binding proteins in the bloodstream.',
    clinicalRationale: 'High-dose salicylates displace thyroxine (T4) and triiodothyronine (T3) from thyroxine-binding globulin (TBG), causing a transient increase in free hormone fraction followed by normal equilibrium.',
    patientActionableAdvice: 'Low-dose baby aspirin (81mg) has negligible impact. Avoid chronic high-dose aspirin without lab re-evaluation.',
  },
  {
    id: 'vyvanse-zoloft',
    drug1: 'vyvanse',
    drug2: 'zoloft',
    severity: 'moderate',
    mechanismType: 'synergistic',
    title: 'Sympathomimetic & Serotonergic Synergy',
    description: 'May lead to heightened anxiety, pulse elevations, and insomnia if doses are not balanced.',
    clinicalRationale: 'Amphetamine stimulation synergizes with serotonergic signaling, elevating blood pressure and requiring attention to jitteriness or tremor.',
    patientActionableAdvice: 'Take medications at prescribed intervals and report persistent rapid heartbeat or panic sensations.',
  },
  {
    id: 'cipro-tylenol',
    drug1: 'cipro',
    drug2: 'tylenol',
    severity: 'minor',
    mechanismType: 'metabolic',
    title: 'Mild CYP1A2 Metabolic Interaction',
    description: 'Cipro can slightly prolong the half-life of acetaminophen by inhibiting minor cytochrome pathways.',
    clinicalRationale: 'Ciprofloxacin is a known CYP1A2 inhibitor. Minor oxidative pathways of acetaminophen are modulated, but clinical significance is minimal at standard doses.',
    patientActionableAdvice: 'Safe to use at standard recommended pain doses (do not exceed 3,000 mg/day).',
  },
  {
    id: 'xanax-tylenol',
    drug1: 'xanax',
    drug2: 'tylenol',
    severity: 'minor',
    mechanismType: 'synergistic',
    title: 'Mild Sedative Additive Effect',
    description: 'Generally compatible, though some patients experience mild extra drowsiness if sleep-deprived.',
    clinicalRationale: 'No significant pharmacokinetic clash; low-risk combination for headaches or mild muscular tension.',
    patientActionableAdvice: 'Standard doses are generally safe together. Always read label to avoid combination cold meds that include antihistamines.',
  },
];

// Helper to calculate node degree and assign hub status
export function calculateHubMetrics(drugs: Drug[], interactions: DrugInteraction[]): Drug[] {
  const degreeMap = new Map<string, number>();
  drugs.forEach((d) => degreeMap.set(d.id, 0));

  interactions.forEach((i) => {
    degreeMap.set(i.drug1, (degreeMap.get(i.drug1) || 0) + 1);
    degreeMap.set(i.drug2, (degreeMap.get(i.drug2) || 0) + 1);
  });

  // Calculate threshold for hubs: top ~30% degree or degree >= 3
  return drugs.map((d) => {
    const deg = degreeMap.get(d.id) || 0;
    const isHub = deg >= 3 || ['warfarin', 'aspirin', 'zoloft', 'lipitor', 'xanax', 'tramadol'].includes(d.id);
    return {
      ...d,
      degree: deg,
      isHub: isHub,
    };
  });
}

// Initialized DRUGS with Hub metrics
export const DRUGS: Drug[] = calculateHubMetrics(RAW_DRUGS, INTERACTIONS);

// Preset Datasets
export interface PresetDataset {
  id: string;
  name: string;
  badge: string;
  description: string;
  drugs: Drug[];
  interactions: DrugInteraction[];
}

export const PRESET_DATASETS: PresetDataset[] = [
  {
    id: 'default-all',
    name: 'Top 24 Common Drugs (Hub & Spoke Network)',
    badge: 'Flagship Network',
    description: 'Complete Flourish-style hub-and-spoke web featuring primary anticoagulant, NSAID, statin, and psychiatric hubs with orbital spokes.',
    drugs: DRUGS,
    interactions: INTERACTIONS,
  },
  {
    id: 'cardio-deep',
    name: 'Cardiovascular & Anticoagulant Deep Cluster',
    badge: 'Cardio Focus',
    description: 'Sub-network focused on bleeding synergy, platelet blockade, statin myopathy, and acute vascular collapse.',
    drugs: calculateHubMetrics(
      RAW_DRUGS.filter((d) =>
        ['warfarin', 'aspirin', 'plavix', 'eliquis', 'lipitor', 'lisinopril', 'nitrostat', 'viagra', 'diflucan', 'cipro', 'ibuprofen'].includes(d.id)
      ),
      INTERACTIONS.filter((i) =>
        ['warfarin', 'aspirin', 'plavix', 'eliquis', 'lipitor', 'lisinopril', 'nitrostat', 'viagra', 'diflucan', 'cipro', 'ibuprofen'].includes(i.drug1) &&
        ['warfarin', 'aspirin', 'plavix', 'eliquis', 'lipitor', 'lisinopril', 'nitrostat', 'viagra', 'diflucan', 'cipro', 'ibuprofen'].includes(i.drug2)
      )
    ),
    interactions: INTERACTIONS.filter((i) =>
      ['warfarin', 'aspirin', 'plavix', 'eliquis', 'lipitor', 'lisinopril', 'nitrostat', 'viagra', 'diflucan', 'cipro', 'ibuprofen'].includes(i.drug1) &&
      ['warfarin', 'aspirin', 'plavix', 'eliquis', 'lipitor', 'lisinopril', 'nitrostat', 'viagra', 'diflucan', 'cipro', 'ibuprofen'].includes(i.drug2)
    ),
  },
  {
    id: 'neuro-psych',
    name: 'Psychotropic & Neuroactive Matrix',
    badge: 'Neuro / Psych',
    description: 'Sub-network mapping serotonin syndrome, additive CNS sedation, respiratory depression, and adrenergic toxicity.',
    drugs: calculateHubMetrics(
      RAW_DRUGS.filter((d) =>
        ['zoloft', 'prozac', 'lexapro', 'adderall', 'vyvanse', 'xanax', 'valium', 'ambien', 'tramadol', 'st-johns-wort'].includes(d.id)
      ),
      INTERACTIONS.filter((i) =>
        ['zoloft', 'prozac', 'lexapro', 'adderall', 'vyvanse', 'xanax', 'valium', 'ambien', 'tramadol', 'st-johns-wort'].includes(i.drug1) &&
        ['zoloft', 'prozac', 'lexapro', 'adderall', 'vyvanse', 'xanax', 'valium', 'ambien', 'tramadol', 'st-johns-wort'].includes(i.drug2)
      )
    ),
    interactions: INTERACTIONS.filter((i) =>
      ['zoloft', 'prozac', 'lexapro', 'adderall', 'vyvanse', 'xanax', 'valium', 'ambien', 'tramadol', 'st-johns-wort'].includes(i.drug1) &&
      ['zoloft', 'prozac', 'lexapro', 'adderall', 'vyvanse', 'xanax', 'valium', 'ambien', 'tramadol', 'st-johns-wort'].includes(i.drug2)
    ),
  },
  {
    id: 'high-risk-only',
    name: 'High-Risk Critical Interactions Only',
    badge: 'Critical Red',
    description: 'Isolated high-severity dangerous combinations carrying FDA Boxed Warnings and life-threatening contraindications.',
    drugs: calculateHubMetrics(
      RAW_DRUGS.filter((d) =>
        INTERACTIONS.filter((i) => i.severity === 'severe').some((i) => i.drug1 === d.id || i.drug2 === d.id)
      ),
      INTERACTIONS.filter((i) => i.severity === 'severe')
    ),
    interactions: INTERACTIONS.filter((i) => i.severity === 'severe'),
  },
];

// Helper to look up an interaction between any two drugs
export function getInteractionBetween(
  drugIdA: string,
  drugIdB: string,
  interactionList: DrugInteraction[] = INTERACTIONS
): DrugInteraction | null {
  if (!drugIdA || !drugIdB || drugIdA === drugIdB) return null;
  return (
    interactionList.find(
      (item) =>
        (item.drug1 === drugIdA && item.drug2 === drugIdB) ||
        (item.drug1 === drugIdB && item.drug2 === drugIdA)
    ) || null
  );
}

// Helper to find all interactions for a specific drug
export function getInteractionsForDrug(
  drugId: string,
  interactionList: DrugInteraction[] = INTERACTIONS
): DrugInteraction[] {
  return interactionList.filter((item) => item.drug1 === drugId || item.drug2 === drugId);
}

// Helper to find all interactions in a list of drugs (e.g. personal cabinet)
export function findInteractionsInCabinet(
  drugIds: string[],
  drugList: Drug[] = DRUGS,
  interactionList: DrugInteraction[] = INTERACTIONS
): {
  conflicts: { interaction: DrugInteraction; drugA: Drug; drugB: Drug }[];
  severeCount: number;
  moderateCount: number;
  minorCount: number;
} {
  const conflicts: { interaction: DrugInteraction; drugA: Drug; drugB: Drug }[] = [];
  let severeCount = 0;
  let moderateCount = 0;
  let minorCount = 0;

  const drugMap = new Map(drugList.map((d) => [d.id, d]));

  for (let i = 0; i < drugIds.length; i++) {
    for (let j = i + 1; j < drugIds.length; j++) {
      const match = getInteractionBetween(drugIds[i], drugIds[j], interactionList);
      if (match) {
        const drugA = drugMap.get(match.drug1);
        const drugB = drugMap.get(match.drug2);
        if (drugA && drugB) {
          conflicts.push({ interaction: match, drugA, drugB });
          if (match.severity === 'severe') severeCount++;
          else if (match.severity === 'moderate') moderateCount++;
          else minorCount++;
        }
      }
    }
  }

  return { conflicts, severeCount, moderateCount, minorCount };
}

// Parser for custom JSON data
export function parseCustomJson(jsonString: string): { drugs: Drug[]; interactions: DrugInteraction[] } {
  const parsed = JSON.parse(jsonString);
  let drugs: Drug[] = [];
  let interactions: DrugInteraction[] = [];

  if (Array.isArray(parsed)) {
    // Array of interaction pairs or drugs
    if (parsed.length > 0 && ('drug1' in parsed[0] || 'from' in parsed[0])) {
      interactions = parsed.map((item, idx) => ({
        id: item.id || `custom-inter-${idx}`,
        drug1: item.drug1 || item.from,
        drug2: item.drug2 || item.to,
        severity: item.severity || 'moderate',
        mechanismType: item.mechanismType || 'synergistic',
        title: item.title || `${item.drug1 || item.from} + ${item.drug2 || item.to}`,
        description: item.description || 'Custom loaded interaction.',
        clinicalRationale: item.clinicalRationale || 'Uploaded clinical evidence.',
        patientActionableAdvice: item.patientActionableAdvice || 'Consult physician.',
      }));

      // Infer drugs from interactions
      const uniqueDrugIds = Array.from(new Set(interactions.flatMap((i) => [i.drug1, i.drug2])));
      drugs = uniqueDrugIds.map((id) => {
        const existing = RAW_DRUGS.find((d) => d.id === id);
        return (
          existing || {
            id,
            brandName: id.charAt(0).toUpperCase() + id.slice(1),
            genericName: id,
            category: 'Imported Agent',
            classKey: 'analgesic',
            description: `Imported drug record for ${id}`,
            commonSideEffects: ['Refer to package insert'],
            patientAdvice: 'Use as directed by healthcare provider.',
          }
        );
      });
    } else {
      drugs = parsed;
    }
  } else if (parsed && typeof parsed === 'object') {
    if (Array.isArray(parsed.drugs)) {
      drugs = parsed.drugs.map((d: any) => ({
        id: d.id || d.name?.toLowerCase().replace(/\s+/g, '-'),
        brandName: d.brandName || d.name || 'Unknown Drug',
        genericName: d.genericName || d.brandName || 'Unknown Active Ingredient',
        category: d.category || 'Pharmaceutical',
        classKey: d.classKey || 'analgesic',
        description: d.description || '',
        commonSideEffects: Array.isArray(d.commonSideEffects) ? d.commonSideEffects : [d.commonSideEffects || 'None noted'],
        patientAdvice: d.patientAdvice || 'Consult prescribing doctor.',
        fdaBoxedWarning: !!d.fdaBoxedWarning,
        boxedWarningSummary: d.boxedWarningSummary,
      }));
    }
    if (Array.isArray(parsed.interactions)) {
      interactions = parsed.interactions.map((i: any, idx: number) => ({
        id: i.id || `custom-inter-${idx}`,
        drug1: i.drug1 || i.from,
        drug2: i.drug2 || i.to,
        severity: ['severe', 'moderate', 'minor'].includes(i.severity) ? i.severity : 'moderate',
        mechanismType: ['synergistic', 'metabolic', 'clearance'].includes(i.mechanismType) ? i.mechanismType : 'synergistic',
        title: i.title || `${i.drug1} + ${i.drug2} Interaction`,
        description: i.description || 'Adverse interaction documented.',
        clinicalRationale: i.clinicalRationale || 'Pharmacological incompatibility.',
        patientActionableAdvice: i.patientActionableAdvice || 'Consult physician before co-administration.',
      }));
    }
  }

  if (drugs.length === 0) {
    throw new Error('No valid drugs found in provided JSON.');
  }

  return {
    drugs: calculateHubMetrics(drugs, interactions),
    interactions,
  };
}

// Parser for custom CSV data
export function parseCustomCsv(csvString: string): { drugs: Drug[]; interactions: DrugInteraction[] } {
  const lines = csvString.trim().split(/\r?\n/).filter((l) => l.trim().length > 0);
  if (lines.length < 2) {
    throw new Error('CSV must contain at least a header and one row.');
  }

  const headers = lines[0].split(',').map((h) => h.trim().toLowerCase().replace(/^["']|["']$/g, ''));
  
  // Check if CSV is an interaction list (contains drug1/drug2 or source/target)
  const isInteractionCsv = headers.includes('drug1') || headers.includes('source') || (headers.includes('drug_a') && headers.includes('drug_b'));

  if (isInteractionCsv) {
    const d1Index = headers.findIndex((h) => ['drug1', 'source', 'drug_a'].includes(h));
    const d2Index = headers.findIndex((h) => ['drug2', 'target', 'drug_b'].includes(h));
    const sevIndex = headers.findIndex((h) => ['severity', 'risk', 'level'].includes(h));
    const descIndex = headers.findIndex((h) => ['description', 'title', 'effect'].includes(h));
    const mechIndex = headers.findIndex((h) => ['mechanism', 'type', 'mechanismtype'].includes(h));

    const interactions: DrugInteraction[] = [];
    const drugSet = new Set<string>();

    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',').map((c) => c.trim().replace(/^["']|["']$/g, ''));
      if (cols.length < 2) continue;

      const drug1 = cols[d1Index]?.toLowerCase().replace(/\s+/g, '-');
      const drug2 = cols[d2Index]?.toLowerCase().replace(/\s+/g, '-');
      if (!drug1 || !drug2 || drug1 === drug2) continue;

      drugSet.add(drug1);
      drugSet.add(drug2);

      const rawSev = sevIndex >= 0 ? cols[sevIndex]?.toLowerCase() : 'moderate';
      const severity: 'severe' | 'moderate' | 'minor' = rawSev.includes('sev') || rawSev.includes('high') ? 'severe' : rawSev.includes('min') || rawSev.includes('low') ? 'minor' : 'moderate';

      const rawMech = mechIndex >= 0 ? cols[mechIndex]?.toLowerCase() : 'synergistic';
      const mechanismType: 'synergistic' | 'metabolic' | 'clearance' = rawMech.includes('met') || rawMech.includes('cyp') ? 'metabolic' : rawMech.includes('ren') || rawMech.includes('clear') ? 'clearance' : 'synergistic';

      interactions.push({
        id: `csv-${drug1}-${drug2}-${i}`,
        drug1,
        drug2,
        severity,
        mechanismType,
        title: descIndex >= 0 && cols[descIndex] ? cols[descIndex] : `${drug1} + ${drug2} Interaction`,
        description: descIndex >= 0 && cols[descIndex] ? cols[descIndex] : `Adverse interaction between ${drug1} and ${drug2}.`,
        clinicalRationale: 'Documented in external pharmacovigilance CSV dataset.',
        patientActionableAdvice: 'Consult a healthcare professional for dose timing or alternatives.',
      });
    }

    const drugs: Drug[] = Array.from(drugSet).map((id) => {
      const existing = RAW_DRUGS.find((d) => d.id === id);
      return (
        existing || {
          id,
          brandName: id.charAt(0).toUpperCase() + id.slice(1).replace(/-/g, ' '),
          genericName: id.replace(/-/g, ' '),
          category: 'Pharmaceutical',
          classKey: 'analgesic',
          description: `Imported medication from CSV record.`,
          commonSideEffects: ['Refer to official monograph'],
          patientAdvice: 'Use under licensed medical guidance.',
        }
      );
    });

    return {
      drugs: calculateHubMetrics(drugs, interactions),
      interactions,
    };
  } else {
    // CSV is a drug list
    const nameIndex = headers.findIndex((h) => ['brandname', 'name', 'drug', 'brand_name'].includes(h));
    const genericIndex = headers.findIndex((h) => ['genericname', 'generic', 'active_ingredient'].includes(h));
    const catIndex = headers.findIndex((h) => ['category', 'class', 'group'].includes(h));

    const drugs: Drug[] = [];
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',').map((c) => c.trim().replace(/^["']|["']$/g, ''));
      if (cols.length < 1 || !cols[nameIndex >= 0 ? nameIndex : 0]) continue;

      const brand = cols[nameIndex >= 0 ? nameIndex : 0];
      const id = brand.toLowerCase().replace(/\s+/g, '-');
      drugs.push({
        id,
        brandName: brand,
        genericName: genericIndex >= 0 && cols[genericIndex] ? cols[genericIndex] : brand,
        category: catIndex >= 0 && cols[catIndex] ? cols[catIndex] : 'General',
        classKey: 'analgesic',
        description: 'Imported from custom drug CSV.',
        commonSideEffects: ['Refer to packaging'],
        patientAdvice: 'Follow prescribing instructions.',
      });
    }

    return {
      drugs: calculateHubMetrics(drugs, []),
      interactions: [],
    };
  }
}

// Export helpers
export function exportDatasetAsJson(drugs: Drug[], interactions: DrugInteraction[]): string {
  return JSON.stringify({ drugs, interactions }, null, 2);
}

export function exportDatasetAsCsv(drugs: Drug[], interactions: DrugInteraction[]): string {
  const header = 'drug1,drug2,severity,mechanismType,title,description\n';
  const rows = interactions
    .map(
      (i) =>
        `"${i.drug1}","${i.drug2}","${i.severity}","${i.mechanismType}","${i.title.replace(/"/g, '""')}","${i.description.replace(/"/g, '""')}"`
    )
    .join('\n');
  return header + rows;
}

