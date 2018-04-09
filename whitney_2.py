import os
import mia

class plate :
    def __init__(self, path, pmap_name=None) :
        self.path = path
        self.name = os.path.basename(self.path[:-1])
        
        # pmap = plate map
        self.pmap_path = self.get_pmap_path(pmap_name) 
        
        # condit_dict--> keys = condits : values = well_names
        self.condit_dict = self.create_condit_dict()
        self.condits = self.create_condits()

        
    def get_pmap_path(self, pmap_name) :
        if pmap_name == None :
            return self.path + self.name + "_plate-map.csv"
        else : return self.path + pmap_name
    
    # requires self.pmap_path to already be instantiated
    # takes pmap_path, opens it and turns it into condit_dict
    def create_condit_dict(self) :
        "takes pmap_path, opens it and turns it into condit_dict"
        # open plate map and get headings
        pmap_rows = mia.csv_to_arr(self.pmap_path)
        col_headings = pmap_rows[0][1:]
        del pmap_rows[0]
        pmap_cols = mia.rotate(pmap_rows)
        row_headings = pmap_cols[0]
        del pmap_cols[0]
        
        
        pmap_cols = delete_empty_arrs(pmap_cols, col_headings, blank='')
        #print(pmap_cols) 
        pmap_rows = mia.rotate(pmap_cols)
        pmap_rows = delete_empty_arrs(pmap_rows, row_headings, blank='')
        pmap_cols = mia.rotate(pmap_rows)
        
        condit_dict = {}
        for row in pmap_rows :
            for item in row :
                condit_dict[item] = []
        #verbose_dict={}
        for r in range(len(pmap_rows)) :
            for c in range(len(pmap_rows[r])) :
                well_name = row_headings[r] + double_digits(col_headings[c])
                condit_dict[pmap_rows[r][c]].append(well_name)
                #print(well_name)
        #print(condit_dict)
        
        self.pmap_rows = pmap_rows
        self.condit_index = sorted(condit_dict.keys())
        return condit_dict

    
    def create_condits(self) :
        conditions = []
        for condit in self.condit_index :
            #print(condit)
            conditions.append(condition(condit,self,self.condit_dict[condit]))
            
            
        return conditions
    
    
        
class condition :
    def __init__(self, name, plate, wells) :
        self.name = name
        self.plate = plate
        self.wells = wells
        
        self.cells = self.create_cells()
        
        
    def create_cells(self) :
        return None
        
class cell :
    def __init__(self, plate, condition, well_name, format_version) :
        self.plate = plate
        self.condit = condition
        self.well_name = well_name
        self.format_version = format_version
        self.src_file_path = self.create_src_file_path()
        self.data = self.read_data()
    
    def create_src_file_path(self) :
        return None
        
    def read_data(self) :
        return None
        
    
def delete_empty_arrs(arr2d, headings, blank=None) :
    j = 0
    for i in range(len(arr2d)) :
        delete = True
        #print(str(i-j) + " " +str(len(arr2d)))

        for item in arr2d[i-j] :
            if not item == blank :
                delete = False
                break
        if delete :
            #print("\t" + stri-ji) + " " +str(len(arr2d)))
            del arr2d[i-j]
            del headings[i-j]
            j +=1;
    return arr2d;
    
    
# s assumed to type str representing a whole number 
def double_digits(s) :
    if len(s) == 1 :
        s = "0" + s
    return s