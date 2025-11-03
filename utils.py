import os
import numpy as np
import trimesh

# Function to get hull area
def get_hull_area(mesh):
    convex_hull = trimesh.convex.convex_hull(mesh)
    return float(convex_hull.area)  # Convert to float to ensure it's a numeric value

def get_gyrification_index(mesh):
    """
    Gyrification index as surface ratio between a mesh and its convex hull
    
    Parameters
    ----------
    mesh : Trimesh
        Triangular watertight mesh
    
    Returns
    -------
    gyrification_index : Float
        surface ratio between a mesh and its convex hull
    hull_area : Float
        area of the convex hull
    """
    hull_area = get_hull_area(mesh)
    gyrification_index = float(mesh.area) / hull_area  # Convert both to float
    return gyrification_index, hull_area

def calculate_band_wavelength(eigVal, group_indices):
    """
    Calculate the wavelength for each band based on eigenvalues
    
    Parameters
    ----------
    eigVal : ndarray
        Eigenvalues from the spectrum analysis
    group_indices : list of arrays
        Indices of eigenvalues in each band
    
    Returns
    -------
    band_wavelengths : list
        Average wavelength for each band in mm
    """
    band_wavelengths = []
    
    for indices in group_indices:
        if len(indices) == 0:  # Check if array is empty
            band_wavelengths.append(0)
            continue
            
        # Calculate frequency from eigenvalues using equation in Appendix A.1
        band_frequencies = np.sqrt(eigVal[indices] / (2 * np.pi))
        
        # Wavelength = 1/frequency (in mm)
        if np.mean(band_frequencies) > 0:
            avg_wavelength = 1 / np.mean(band_frequencies)
        else:
            avg_wavelength = 0
            
        band_wavelengths.append(avg_wavelength)
    
    return band_wavelengths

def calculate_parcels_per_band(loc_dom_band, levels):
    """
    Calculate the number of parcels (connected components) for each band
    
    Parameters
    ----------
    loc_dom_band : ndarray
        Local dominant band map
    levels : int
        Number of frequency bands
    
    Returns
    -------
    parcels_per_band : list
        Number of parcels for each band
    """
    from scipy import ndimage
    
    parcels_per_band = []
    
    for i in range(levels):
        # Create binary mask for this band
        band_mask = (loc_dom_band == i).astype(int)
        
        # Check if the band exists at all
        if np.sum(band_mask) == 0:
            parcels_per_band.append(0)
            continue
            
        # Label connected components
        labeled_array, num_parcels = ndimage.label(band_mask)
        
        parcels_per_band.append(num_parcels)
    
    return parcels_per_band

def calculate_band_coverage(mesh, loc_dom_band, band_idx):
    """
    Calculate the coverage metrics for a specific frequency band using local dominance map.
    
    Parameters:
    mesh: Mesh object containing vertices and faces
    loc_dom_band: Array of local dominant bands for each vertex
    band_idx: Index of the band to analyze (e.g., 4 for B4)
    
    Returns:
    float: Number of vertices where this band is dominant
    float: Percentage of total vertices
    float: Surface area covered by the band in mm²
    float: Percentage of total surface area
    """
    # Count vertices where this band is dominant
    band_vertices = loc_dom_band == band_idx
    num_vertices = np.sum(band_vertices)
    vertex_percentage = (num_vertices / len(loc_dom_band)) * 100
    
    # Calculate surface area coverage
    total_area = 0
    faces = mesh.faces
    vertices = mesh.vertices
    
    for face in faces:
        # If any vertex in the face has this dominant band, include face area
        if any(band_vertices[face]):
            v1, v2, v3 = vertices[face]
            # Calculate face area using cross product
            area = 0.5 * np.linalg.norm(np.cross(v2 - v1, v3 - v1))
            total_area += area
    
    area_percentage = (total_area / mesh.area) * 100
    return num_vertices, vertex_percentage, total_area, area_percentage

def ensure_dir_exists(directory):
    """
    Make sure a directory exists, creating it if necessary
    Handle the case where the directory might be created between check and creation
    """
    try:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
    except FileExistsError:
        # Directory already exists (race condition handled)
        print(f"Directory already exists: {directory}")
        pass