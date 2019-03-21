import numpy as np

class song_structure():
    
    def __init__(self, numVerses = 0, hasBridge = False, hasPrechorus = False):
        """Initializes the attributes.
        """
        
        self.nVerses = numVerses
        self.hasBridge = hasBridge
        self.hasPrechorus = hasPrechorus
        
 
    def make_structure(random = False):
        
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
            
            #decide if we'll add a prechorus
            if self.hasPrechorus == True :
                chorusChunk = np.random.choice("", "P") + "C"
            else:
                chorusChunk = "C"
                
            n = 1
            structure = "V"
            
            
            while n < numVerses:
                
                if np.random.random() < 0.6:
                    structure = structure + "V"
                    n = n + 1
                else:
                    structure = structure + chorusChunk
            
            if self.hasBridge == True and np.random.random <= 0.5:
                structure = structure + "BC"
                
        
        return structure      
    