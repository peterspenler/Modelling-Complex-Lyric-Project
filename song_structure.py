class song_structure():
    
    def __init__(self, numVerses = 0, hasBridge = False, hasPrechorus = False):
        """Initializes the attributes.
        """
        
        self.nVerses = numVerses
        self.hasBridge = hasBridge
        self.hasPrechorus = hasPrechorus
        
 
    def make_structure():
        
        """We will define the structure using a series of characters,
        C = chorus
        V = verse
        P = prechorus
        B = Bridge
        
        The standard structure will have a pattern of:
        VCVCVC...VC
        If there is a prechorus it will be added before all choruses
        If there is a bridge the song will instead end with:
        ...VCBC
        """
        
        if self.hasPrechorus == True:
            chorusChunk = "PC"
        else:
            chorusChunk = "C"
        
        structure = ""
            
        for i in range(self.numVerses):
            structure = structure + "V" + chorusChunk
            
        if self.hasBridge == True:
            structure = structure + "B" + chorusChunk
        
        return structure      
                