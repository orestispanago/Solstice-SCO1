import os
from traces import Transversal
from config import trace

tr_args = trace.transversal.values()
ln_args = trace.longitudinal.values()

geometries = [g for g in os.listdir("geometries") if g.startswith("stl")]
geometries.sort(reverse=True)


transversal_traces = [Transversal(*tr_args, g) for g in geometries]
# ideal_longitudinal_traces = [Longitudinal(*ln_args, g) for g in geometries]


def run_vtk_obj_heat(trace):
    trace.run()
    trace.export_vtk()
    trace.export_obj()
    # trace.export_heat()


if __name__ == "__main__":

    for i in transversal_traces:
        run_vtk_obj_heat(i)
