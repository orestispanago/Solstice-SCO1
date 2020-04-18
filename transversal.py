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



class Transversal():
    def __init__(self, min_angle, max_angle, step, rays):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.step = step
        self.rays = rays

    def run(self):
        angles = np.arange(self.min_angle, self.max_angle+1, self.step).tolist()
        azzen = [f"{a:.1f},0" for a in angles]
        out_file = os.path.join(exp_dir,'transversal.txt')
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
        for az in [self.min_angle,self.max_angle]:
            fname = f"transv_{az}.vtk"
            vtkpath = os.path.join(exp_shapes_dir,fname)
            cmd = f'solstice  -n {nrays} -p default -t1 -D {az},0 -R {receiver} {geometry}'.split()
            with open(vtkpath, 'w') as f:
                subprocess.run(cmd,stdout=f)
            del_first_line(vtkpath)

    @staticmethod
    def export_obj():
        os.chdir(geom_dir)
        objpath = os.path.join(exp_shapes_dir,'geom.obj')
        cmd = f'solstice -n 100 -g format=obj -t1 -D 0,0 -R {receiver} {geometry}'.split()
        with open(objpath, 'w') as f:
            subprocess.run(cmd,stdout=f)
        
def del_first_line(fname):
    # Deletes first line from vtk file to be opened by Paraview
    with open(fname, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(fname, 'w') as fout:
        fout.writelines(data[1:])


transversal = Transversal(135,225,1,10000)
transversal.run()
        
      
        
        
        
        
        
        
        
        
        
        
        
