import numpy as np
import os
import subprocess
import time



exp_dir = os.path.join(os.getcwd(),'raw')
geom_dir = os.path.join(os.getcwd(),"geometry")
geometry = os.path.join(geom_dir,"geometry_my_stl.yaml") 
receiver = os.path.join(geom_dir,"receiver.yaml") 
exp_shapes_dir = os.path.join(os.getcwd(),"export-shapes")

# cmd = 'solstice -D 180,0 -n 100 -t1 -v -R receiver.yaml geometry_my_stl.yaml'.split()    


class Longitudinal():
    def __init__(self, min_angle, max_angle, step, rays):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.step = step
        self.rays = rays

    def run(self):
        angles = np.arange(self.min_angle, self.max_angle+1, self.step).tolist()
        azzen = [f"180,{a:.1f}" for a in angles]
        out_file = os.path.join(exp_dir,'longitudinal.txt')
        os.chdir(geom_dir)
        with open(out_file, 'w') as f:
            # Solstice cannot take too long string of angle arguments, so split into chunks
            for i in range(0, len(azzen), 50):
                chunk = azzen[i:i + 50]
                chunk = ":".join(chunk)
                cmd = f'solstice -D {chunk} -n {self.rays} -v -R {receiver} {geometry}'.split()
                subprocess.run(cmd,stdout=f)
                
    def export_vtk(self,nrays=100):
        os.chdir(geom_dir)
        for elev in [self.min_angle,self.max_angle]:
            fname = f"long_{elev}.vtk"
            vtkpath = os.path.join(exp_shapes_dir,fname)
            cmd = f'solstice  -n {nrays} -p default -t1 -D 180,{elev} -R {receiver} {geometry}'.split()
            with open(vtkpath, 'w') as f:
                subprocess.run(cmd,stdout=f)
            del_first_line(vtkpath)

        
def del_first_line(fname):
    # Deletes first line from vtk file to be opened by Paraview
    with open(fname, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(fname, 'w') as fout:
        fout.writelines(data[1:])


long = Longitudinal(0,25,1,10000)
long.run()
        
      
        
        
        
        
        
        
        
        
        
        
        