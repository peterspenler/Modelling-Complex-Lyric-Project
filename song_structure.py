import numpy as np

class song_structure():
    
    def __init__(self, numVerses = 0, hasBridge = False, hasPrechorus = False):
        """Initializes the attributes.
        """
        
        self.numVerses = numVerses
        self.hasBridge = hasBridge
        self.hasPrechorus = hasPrechorus
        
 
    def make_structure(self, random = False):
        
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
        
        structure = ""
        
        if random == False:
        
            if self.hasPrechorus == True:
                chorusChunk = "PC"
            else:
                chorusChunk = "C"

            

            for i in range(self.numVerses):
                structure = structure + "V" + chorusChunk

            if self.hasBridge == True:
                structure = structure + "B" + chorusChunk
        
        else:
            
            chorusChunk = "C"
            
            #decide if we'll add a prechorus
            if self.hasPrechorus == True and np.random.random() <= 0.5:
                chorusChunk = 'PC' 
                
            n = 0
            
            while n < self.numVerses:
                newVerses = np.random.randint(self.numVerses - n) + 1
                for i in range(newVerses):
                    structure = structure + "V"
                    n = n + 1
            
                structure = structure + chorusChunk
            
            if self.hasBridge == True and np.random.random() <= 0.5:
                structure = structure + "BC"
                
        
        return structure      
    