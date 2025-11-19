"""
Create a distance-based texture file for brain mesh visualization.
Calculates the distance from each vertex to the mesh center of mass.
"""

from utils import process_dist_tex
import os
import slam.io as sio
from utils import mesh_orientation, read_gii_file, plot_distance_texture

mesh_dir = '/home/INT/dienye.h/python_files/qc_identified_meshes/dHCP/mesh' # mesh directory
output_tex_dir= '/home/INT/dienye.h/python_files/distance_texture_test/' # output texture directory
output_snapshot_dir = '/home/INT/dienye.h/python_files/distance_snapshot_test' # output snapshout directory

# Mesh processing parameters
MESH_PREFIX = "smooth_5_"
MESH_SUFFIX_TO_REMOVE = "reo-SVR-output-brain-mask-brain_bounti-white."
TEXTURE_PREFIX = "dist_tex_smooth_5_"

# Plot parameters
PLOT_TITLE = 'Distance Texture Visualization'
SHOW_DUAL_VIEW = True


if __name__ == "__main__":
    
    # Collect vertex counts from all meshes
    processed_count = 0
    
    #Create distance texture
    for i in os.listdir(mesh_dir):
        #Load Mesh file
        mesh_file = os.path.join(mesh_dir, i)

        # Create output directory if it doesn't exist
        os.makedirs(output_tex_dir, exist_ok=True)

        #Create and save distance texture
        output_tex_path = os.path.join(output_tex_dir, 'dist_tex_{}'.format(i)) if i else None
        process_dist_tex(mesh_file, output_tex_path) 
    

    #Create snapshot
    for filename in os.listdir(mesh_dir):

        original_filename = filename
        
        for file in os.listdir(output_tex_dir):
            # Remove the prefix and suffix
            clean_filename = file.replace(TEXTURE_PREFIX, "").replace(MESH_SUFFIX_TO_REMOVE, "").replace(".surf.gii", "")
            
            # Clean mesh filename
            filename_cleaned = filename.replace(MESH_PREFIX, "").replace(
                MESH_SUFFIX_TO_REMOVE, ""
            ).replace(".surf.gii", "") if filename.startswith(MESH_PREFIX) else filename

            print("mesh", filename_cleaned)
            print('tex', clean_filename)

            if filename_cleaned == clean_filename:
                participant_session = clean_filename.split('_')[0] + '_' + clean_filename.split('_')[1]
                
                # Load mesh file
                mesh_file = os.path.join(mesh_dir, original_filename)
                mesh = sio.load_mesh(mesh_file)
                hem_det = clean_filename.split('_')[-1].split('.')[0]
                
                # Orient mesh
                mesh, camera_medial, camera_lateral = mesh_orientation(mesh, hem_det)
                vertices = mesh.vertices
                faces = mesh.faces

                # Load generated texture
                tex_file = os.path.join(output_tex_dir, file)
                distance_texture = read_gii_file(tex_file)

                # Create visualization with dual view
                fig = plot_distance_texture(
                    vertices=mesh.vertices,
                    faces=mesh.faces,
                    distances=distance_texture,
                    distance_range= (0, 100),
                    camera=camera_medial, 
                    title=PLOT_TITLE,
                    show_dual_view=SHOW_DUAL_VIEW
                )
                
                # Save output
                output_path = os.path.join(output_snapshot_dir, f"{participant_session}_{hem_det}.png")
                fig.write_image(output_path)
                
                processed_count += 1
                print(f"Processed: {participant_session}_{hem_det}")
    
    print("-" * 60)
    print(f"Total images processed: {processed_count}")
    print(f"All outputs saved to: {output_snapshot_dir}")