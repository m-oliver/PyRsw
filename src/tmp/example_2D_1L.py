import Differentiation as Diff
import Steppers
import Fluxes
import numpy as np
from PySW import Simulation
from constants import minute, hour, day

# Create a simulation object
sim = Simulation()
sim.method = 'FV'

# Specify geometry conditions
sim.x_derivs = Diff.FV_x_WENO
sim.y_derivs = Diff.FV_y_WENO

# Specify time-stepping algorithm
sim.time_stepper = Steppers.AB2

# Specify the flux and source function
sim.flux_function = Fluxes.fv_sw_flux
sim.source_function = Fluxes.fv_sw_source

# Specify paramters
sim.Lx  = 600e3   # Domain extent (m)
sim.Ly  = 400e3   # Domain extent (m)
sim.Nx  = 128*2   # Grid points in x
sim.Ny  = 128*2   # Grid points in y
sim.Nz  = 1       # Number of layers
sim.f0  = 0.e-4   # Coriolis
sim.cfl = 0.2     # CFL coefficient
sim.Hs  = [50.]   # Vector of mean layer depths
sim.rho = [1025.] # Vector of layer densities
sim.ptime = 1.*minute
sim.dtime = 1.*minute
sim.output = False
sim.animate = 'Save'
sim.diagnose = False

# Specify initial conditions
# (this can also be put in a separate file,
#   may be useful for more complicated ICs)
def my_ICs(a_sim):

    # Initial velocities are zero

    # Initialize etas
    for ii in range(a_sim.Nz):
        a_sim.sol[a_sim.Ih,:,:,ii] = np.sum(a_sim.Hs[ii:])

    x0 = 1.*a_sim.Lx/2.
    y0 = 1.*a_sim.Ly/2.
    X,Y = np.meshgrid(a_sim.x, a_sim.y,indexing='ij')
    W  = 30.e3 
    amp = 10. 
    tmp = np.exp(-((X-x0)/W)**2 - ((Y-y0)/W)**2).reshape((a_sim.Nx,a_sim.Ny))
    a_sim.sol[sim.Ih,:,:,0] += amp*tmp
sim.IC_func = my_ICs

# Run the simulation
sim.initialize()
sim.end_time = 8.*hour
sim.run()