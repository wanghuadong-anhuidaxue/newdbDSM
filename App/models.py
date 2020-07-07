from App.ext import db
# 报错解决方法https://blog.csdn.net/w18306890492/article/details/83865204


class AllData(db.Model):
    dbid = db.Column(db.INTEGER, primary_key=True)
    DBDSMID = db.Column(db.String(100))
    Disease = db.Column(db.String(100))
    DOID = db.Column(db.String(100))
    Gene = db.Column(db.String(100))
    GeneID = db.Column(db.String(100))
    MIM = db.Column(db.String(100))
    Map_Location = db.Column(db.String(100))
    VariantType = db.Column(db.String(100))
    Protein = db.Column(db.String(100))
    cDNA = db.Column(db.String(100))
    SNPID = db.Column(db.String(100))
    CodonChange = db.Column(db.String(100))
    RefseqTranscript = db.Column(db.String(255))
    P_Value = db.Column(db.String(100))
    Strand = db.Column(db.String(100))
    GRCh38_Position = db.Column(db.String(100))
    GRCh37_Position = db.Column(db.String(100))
    Ref = db.Column(db.String(100))
    Alt = db.Column(db.String(100))
    Year = db.Column(db.String(100))
    PMID = db.Column(db.String(100))
    Ethnicity = db.Column(db.String(100))
    Classification = db.Column(db.String(100))
    StrengthOfEvidence =db.Column(db.String(255))
    KeySentence = db.Column(db.String(255))
    PhyloP100way = db.Column(db.String(100))
    PhastCons100way = db.Column(db.String(100))
    GerpS = db.Column(db.String(100))
    Silva = db.Column(db.String(100))
    DDIG = db.Column(db.String(100))
    FATHMM_MKL = db.Column(db.String(100))
    CADD = db.Column(db.String(100))
    Trap = db.Column(db.String(100))
    DBDSMScore = db.Column(db.String(100))
    Source = db.Column(db.String(100))
    Chromosome = db.Column(db.String(100))


class Tbsubmit(db.Model):
    tbid = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(200))
    joumal = db.Column(db.String(200))
    gene = db.Column(db.String(200))
    email = db.Column(db.String(200))
    mutation = db.Column(db.String(200))
    more = db.Column(db.String(500))



