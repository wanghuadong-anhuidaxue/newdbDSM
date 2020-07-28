
from flask import Blueprint, render_template, session, escape, redirect, url_for, request
from App.tools import numpy as np
from App.models import db, AllData

homeblue = Blueprint("homeblue",__name__)



@homeblue.route('/')
@homeblue.route('/newdbDSM/')
def index():
    return render_template("index.html")





@homeblue.route('/download')
@homeblue.route('/newdbDSM/download')
def download():
    return render_template("download.html")


@homeblue.route('/about')
@homeblue.route('/newdbDSM/about')
def about():
    mRNA_structure = np.load('aboutdata/mRNA_structure.npy')
    microRNA_binding = np.load('aboutdata/microRNA_binding.npy')
    Protein_synthesis = np.load('aboutdata/Protein_synthesis.npy')
    Splicing_regulation = np.load('aboutdata/Splicing_regulation.npy')
    Transcription_factor_regulation = np.load('aboutdata/Transcription_factor_regulation.npy')
    Specific_methods = np.load('aboutdata/Specific_methods.npy')
    General_methods = np.load('aboutdata/General_methods.npy')
    Analysis_articles = np.load('aboutdata/Analysis_articles.npy')
    Review_articels = np.load('aboutdata/Review_articels.npy')
    header = 'chr	pos	id	ref	alt	PrDSM	TraP	SilVA	PhD-SNPg	FATHMM-MKL	CADD	DANN	FATHMM-XF	priPhCons	mamPhCons	verPhCons	priPhyloP	mamPhyloP	verPhyloP	GerpS	TFBs	TE	dPSIZ	DSP	RSCU	dRSCU	CpG?	CpG_exon	SR-	SR+	FAS6-	FAS6+	MES	dMES	MES+	MES-	MEC-MC?	MEC-CS?	MES-KM?	PESE-	PESE+	PESS-	PESS+	f_premrna	f_mrna	functional_score_avg	conservation_avg	function_regions_annotation	translation_efficiency	splicing_feature_avg	sequence_feature_avg	score	vote	feature_list	VEP_ensembl_Transcript_ID	VEP_ensembl_Gene_Name	VEP_ensembl_Gene_ID	VEP_ensembl_Protein_ID	VEP_ensembl_HGVSc	VEP_ensembl_HGVSp	VEP_ensembl_STRAND	VEP_refseq_Transcript_ID	VEP_refseq_Gene_Name	VEP_refseq_Gene_ID	VEP_refseq_Protein_ID(ENSP)	VEP_refseq_HGVSc	VEP_refseq_HGVSp	VEP_refseq_STRAND	SnpEff_ensembl_Transcript_ID	SnpEff_ensembl_Gene_name	SnpEff_ensembl_HGVSc	SnpEff_ensembl_HGVSp	SnpEff_refseq_Transcript_ID	SnpEff_refseq_Gene_name	SnpEff_refseq_HGVSc	SnpEff_refseq_HGVSp	ANNOVAR_ensembl_Transcript_ID	ANNOVAR_ensembl_Gene_ID	ANNOVAR_ensembl_HGVSc	ANNOVAR_ensembl_HGVSp	ANNOVAR_refseq_Transcript_ID	ANNOVAR_refseq_Gene_name	ANNOVAR_refseq_HGVSc	ANNOVAR_refseq_HGVSp	ANNOVAR_ucsc_Transcript_ID	ANNOVAR_ucsc_Gene_name	ANNOVAR_ucsc_HGVSc	ANNOVAR_ucsc_HGVSp'
    _string = '21	33733359	.	G	A	0.0571790659449	0.025	0.007	0.023	0.13716	1.245	0.5969141349903837	0.006277	0.204	0.618	0.409	-0.235	-0.284	-0.091	-2.34	1	2.6325815384356e-05	1.355	44	0.8385	0.3231	1	0.1560	0.0952	0.0000	na	na	4.3300	1.1800	1.1800	-1.1800	0	1	0	0.0000	0.0000	0.0000	0.0000	0.3897	0.1670	0.10775941257324081	0.5856207268768475	1.0	1.1099007890439494e-05	0.18703800557735967	0.3444702654769159	2.2248995095122543	3.0	function_regions_annotation;splicing;sequence_feature;	ENST00000382751	URB1	ENSG00000142207	ENSP00000372199	ENST00000382751.3:c.1713C>T	ENSP00000372199.3:p.His571=	-	NM_014825.2	URB1	9875	NP_055640.2	NM_014825.2:c.1713C>T	NP_055640.2:p.His571=	-	ENST00000382751	URB1	c.1713C>T	p.His571His	NM_014825.2	URB1	c.1713C>T	p.His571His	ENST00000382751	ENSG00000142207	c.1713C>T	p.H571H	NM_014825	URB1	c.1713C>T	p.H571H	uc002ypn.2	URB1	c.1713C>T	p.H571H,\
21	47588379	.	G	A	0.0481049279733	0.112	0.002	0.020	0.02827	0.137	0.30143649897057373	0.006295	0.197	0.001	0.001	-0.455	-2.207	-2.018	-10.2	0	0.000193990013479641	-1.950	158	0.9850	0.4361	1	0.3792	0.0000	0.0000	0.0000	0.0000	na	na	na	na	0	0	0	0.0250	0.0000	0.0000	0.0000	0.3139	0.3744	0.06373296926902026	0.34098766989351154	0.0	8.178651482743691e-05	0.0354500631497134	0.37600208403416113	0.8162545728612338	1.0	sequence_feature;	ENST00000291672	SPATC1L	ENSG00000160284	ENSP00000291672	ENST00000291672.5:c.387C>T	ENSP00000291672.5:p.Thr129=	-	NM_001142854.1|XM_005261188.1	SPATC1L|SPATC1L	84221|84221	NP_001136326.1|XP_005261245.1	NM_001142854.1:c.387C>T|XM_005261188.1:c.387C>T	NP_001136326.1:p.Thr129=|XP_005261245.1:p.Thr129=	-|-	ENST00000291672	SPATC1L	c.387C>T	p.Thr129Thr	NM_001142854.1	SPATC1L	c.387C>T	p.Thr129Thr	ENST00000291672	ENSG00000160284	c.387C>T	p.T129T	NM_001142854	SPATC1L	c.387C>T	p.T129T	uc011afu.2	SPATC1L	c.387C>T	p.T129T,\
22	50986799	.	C	T	0.00790202922475	0	0.003	0.194	0.01850	6.858	0.78680277762675599	0.006835	0.296	0.000	0.000	0.480	-0.806	-1.238	-7.17	0	0.000197864669291965	nan	3033	1.1245	0.1850	1	0.4976	0.0000	0.0000	0.0000	0.0000	na	na	na	na	0	0	0	0.0000	0.0000	0.0000	0.0000	0.1127	0.1127	0.13727389136618953	0.4137443374070327	0.0	8.342007621217856e-05	0.0	0.2559112436095162	0.8070128924589507	1.0	sequence_feature;	ENST00000395676	KLHDC7B	ENSG00000130487	ENSP00000379034	ENST00000395676.2:c.204C>T	ENSP00000379034.2:p.Ser68=	+	NM_138433.3	KLHDC7B	113730	NP_612442.2	NM_138433.3:c.204C>T	NP_612442.2:p.Ser68=	+	ENST00000395676	KLHDC7B	c.204C>T	p.Ser68Ser	NM_138433.3	KLHDC7B	c.204C>T	p.Ser68Ser	ENST00000395676	ENSG00000130487	c.204C>T	p.S68S	NM_138433	KLHDC7B	c.204C>T	p.S68S	uc003bmi.3	KLHDC7B	c.204C>T	p.S68S,\
22	37398226	.	T	C	0.0790437759018	0.175	0.047	0.004	0.01093	0.361	0.48948740851431777	0.017133	0.000	0.000	0.000	-0.891	-0.837	-0.358	-2.97	0	2.15141595358612e-05	1.650	100	0.3255	0.5771	1	0.2976	0.0000	0.0349	0.0000	0.0000	9.1600	0.8000	0.8000	-0.8000	0	1	0	0.0000	0.0189	na	na	0.3381	0.2726	0.10271001767870169	0.38607793311047883	0.0	9.07040571995331e-06	0.20264142171062183	0.3274865284005979	1.0189249713061201	2.0	splicing;sequence_feature;	ENST00000381821|ENST00000405091	TEX33|TEX33	ENSG00000185264|ENSG00000185264	ENSP00000371243|ENSP00000386118	ENST00000381821.1:c.141A>G|ENST00000405091.2:c.141A>G	ENSP00000371243.1:p.Ser47=|ENSP00000386118.2:p.Ser47=	-|-	NM_001163857.1	TEX33	339669	NP_001157329.1	NM_001163857.1:c.141A>G	NP_001157329.1:p.Ser47=	-	ENST00000381821|ENST00000405091	TEX33|TEX33	c.141A>G|c.141A>G	p.Ser47Ser|p.Ser47Ser	NM_001163857.1	TEX33	c.141A>G	p.Ser47Ser	ENST00000381821|ENST00000405091	ENSG00000185264|ENSG00000185264	c.141A>G|c.141A>G	p.S47S|p.S47S	NM_001163857	TEX33	c.141A>G	p.S47S	uc003aqf.3	TEX33	c.141A>G	p.S47S,\
22	23230287	.	T	C	0.0174747621588	0.013	0.001	0.007	0.03633	0.132	0.32094144601043756	0.005718	0.000	0.000	0.000	-1.142	-1.760	-1.623	-5.66	0	0.000672959922494062	nan	153	1.2962	0.1506	1	0.2341	0.0000	0.0108	0.0000	0.0000	3.0200	0.3000	-0.3000	0.3000	0	1	0	0.0000	0.0000	0.0000	0.0000	0.0406	0.3091	0.04917103126171864	0.3425491518270504	0.0	0.00028372103126384743	0.10808612830674222	0.28929142452957085	0.789381456956346	1.0	sequence_feature;	ENST00000526893|ENST00000531372|ENST00000532223	IGLL5|IGLL5|IGLL5	ENSG00000254709|ENSG00000254709|ENSG00000254709	ENSP00000431254|ENSP00000434368|ENSP00000436353	ENST00000526893.1:c.54T>C|ENST00000531372.1:c.54T>C|ENST00000532223.2:c.54T>C	ENSP00000431254.1:p.Pro18=|ENSP00000434368.1:p.Pro18=|ENSP00000436353.1:p.Pro18=	+|+|+	NM_001178126.1|XM_005261300.1	IGLL5|IGLL5	100423062|100423062	NP_001171597.1|XP_005261357.1	NM_001178126.1:c.54T>C|XM_005261300.1:c.54T>C	NP_001171597.1:p.Pro18=|XP_005261357.1:p.Pro18=	+|+	ENST00000526893|ENST00000531372|ENST00000532223	IGLL5|IGLL5|IGLL5	c.54T>C|c.54T>C|c.54T>C	p.Pro18Pro|p.Pro18Pro|p.Pro18Pro	NM_001178126.1	IGLL5	c.54T>C	p.Pro18Pro	ENST00000532223|ENST00000526893|ENST00000531372	ENSG00000254709|ENSG00000254709|ENSG00000254709	c.54T>C|c.54T>C|c.54T>C	p.P18P|p.P18P|p.P18P	NM_001178126	IGLL5	c.54T>C	p.P18P	uc011aiw.2|uc021wmq.1	IGLL5|IGLL5	c.54T>C|c.54T>C	p.P18P|p.P18P,\
1	32936366	.	C	T	0.338782306091	0.13	0.004	0.071	0.88023	12.72	0.68407733444108365	0.009244	0.994	1.000	1.000	0.581	2.825	1.182	4.67	0	0.000198143826074096	-0.591	182	0.6545	0.6909	0	0.4763	0.0061	0.0061	0.0000	0.0000	na	na	na	na	0	0	0	0.0000	0.0000	0.0000	0.0000	0.2504	0.0572	0.28369529936018056	0.9444783685676915	0.0	8.353776917941645e-05	0.04381101962498785	0.15703467409718389	1.4291028994192234	2.0	functional_score;conservation;	ENST00000480336|ENST00000609129	RP1-27O5.3|ZBTB8B	ENSG00000254553|ENSG00000273274	ENSP00000455300|ENSP00000476499	ENST00000480336.1:c.141C>T|ENST00000609129.1:c.141C>T	ENSP00000455300.1:p.Gly47=|ENSP00000476499.1:p.Gly47=	+|+	NM_001145720.1	ZBTB8B	728116	NP_001139192.1	NM_001145720.1:c.141C>T	NP_001139192.1:p.Gly47=	+	ENST00000480336|ENST00000609129	RP1-27O5.3|ZBTB8B	c.141C>T|c.141C>T	p.Gly47Gly|p.Gly47Gly	NM_001145720.1	ZBTB8B	c.141C>T	p.Gly47Gly	ENST00000480336|ENST00000609129	ENSG00000254553|ENSG00000273274	c.141C>T|c.141C>T	p.G47G|p.G47G	NM_001145720	ZBTB8B	c.141C>T	p.G47G	uc001bvl.4	ZBTB8B	c.141C>T	p.G47G,\
1	19282377	.	G	A	0.0418096429407	0.017	0.002	0.024	0.10429	15.67	0.96543007316768348	0.008160	0.819	0.992	0.998	-0.674	-0.312	0.110	-0.387	0	0.000117120862031122	nan	216	0.8385	0.3231	0	1.0192	0.0077	0.0077	0.0000	0.0000	5.9700	0.4800	-0.4800	0.4800	0	1	0	0.0000	0.0000	na	na	0.0086	0.0769	0.1693667907460862	0.8197406467282448	0.0	4.93783517372447e-05	0.14213352885966285	0.1047355432546937	1.2360258879404247	2.0	conservation;splicing;	ENST00000455833	IFFO2	ENSG00000169991	ENSP00000387941	ENST00000455833.2:c.450C>T	ENSP00000387941.2:p.His150=	-	NM_001136265.1	IFFO2	126917	NP_001129737.1	NM_001136265.1:c.450C>T	NP_001129737.1:p.His150=	-	ENST00000455833	IFFO2	c.450C>T	p.His150His	NM_001136265.1	IFFO2	c.450C>T	p.His150His	ENST00000455833	ENSG00000169991	c.450C>T	p.H150H	NM_001136265	IFFO2	c.450C>T	p.H150H	uc001bbd.2	IFFO2	c.450C>T	p.H150H'
    _list = []
    for line in (_string.split(',')):
        line = line.split('\t')
        _list.append(line)
    return render_template("about.html", literatureALLList=[mRNA_structure,microRNA_binding,Protein_synthesis,Splicing_regulation,Transcription_factor_regulation,Specific_methods
                                                            ,General_methods,Analysis_articles,Review_articels],
                           headerList = header.split('\t'),
                           listPredictionInterpretation=_list
                           )



@homeblue.route('/contact')
@homeblue.route('/newdbDSM/contact')
def contact():
    return render_template("contact.html")
