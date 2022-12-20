# This addon is for importing TexTools FBX and several Quality of life changes for rendering or creating mods for Final Fantasy 14 using Blender.
# All credit goes to Meku Maki and Theta, I only added in a couple functions for adjusting game zones imported as fbx.
#

bl_info = {
    "name": "MekTools",
    "author": "Meku Maki, Theta, jTabox",
    "version": (0, 0, 33),
    "blender": (3, 2, 0),
    "location": "3D View > Tools (Right Side) > MekTools",
    "description": "Custom edit of MekTools with added zone utils for imported zones as fbx.",
    "warning": "",
    "support": 'COMMUNITY',
    "category": "Import-Export",
    "website": "",
}


import bpy
import os
from math import radians

class MainPanel(bpy.types.Panel):
    bl_label = "MekTools 0.33"
    bl_idname = "MT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MekTools'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        selected_objects = bpy.context.selected_objects

        #Import/Export
        layout.label(text="Import/Export:")
        
        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator("import_scene.fbx", text = "Import FBX", icon= "IMPORT")
        row.operator("export_scene.fbx", text = "Export FBX", icon= "EXPORT")

        #After import utilities
        layout.label(text = "After Import Utils:")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.clear_parent_keep_transforms", text = "Clear Parents")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.change_to_alpha_hashed", text = "Fix Alpha Blend Mode")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.fixmetallic", text = "Fix Metallic")
                
        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.clear_split_normals", text = "Clear Custom Split Normals")

        #Zone adjustments
        layout.label(text="Zone Adjustments:")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.normal_world_space", text = "Normal To World Space")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.normal_str_half", text = "Normal Strength To Half")

        #Shaders
        layout.label(text="Shaders:")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.matfix", text = "Apply Custom Skin Shader")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.eyefix", text = "Fix Eyes")

class RiggingPanel(bpy.types.Panel):
    bl_label = "For Rigging"
    bl_idname = "MT_RiggingPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MekTools'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        selected_objects = bpy.context.selected_objects

        layout.label(text="Rig replacement", icon="ERROR")

        # Remove bones
        layout.label(text="Bone Removal:")
        
        row = layout.row()
        row.scale_y = 2.0
        row.operator("myops.remove_un_needed_bones", text = "Remove Bones", icon="GROUP_BONE")

        #Append rigs
        layout.label(text="Append Rig:")

        layout.label(text="Male:")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.malerig", text = "Midlander generic", emboss=True, depress=False, icon = "BONE_DATA")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.hrothgar", text = "Hroth/Roega", emboss=True, depress=False, icon = "BONE_DATA")

        layout.label(text="Female:")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.femrig", text = "Hyur/Aura/Miqote", emboss=True, depress=False, icon = "BONE_DATA")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.viera", text = "Viera/Elezen/Roega", emboss=True, depress=False, icon = "BONE_DATA")

        row = layout.row()
        row.scale_y = 1.0
        row.operator("myops.lala", text = "Lalafel", emboss=True, depress=False, icon = "BONE_DATA") 
    
    
# Below here are operations used on the buttons #

class ChangeToAlpha(bpy.types.Operator):
    bl_idname = "myops.change_to_alpha_hashed"
    bl_label = "Change Blend Mode to Alpha Hashed"
    bl_description= "Changes Alpha Blend mode for viewport to Alpha Hashed."
    
    def execute(self, context):
        for item in bpy.data.materials:
            item.blend_method = 'HASHED'
        return {'FINISHED'}

class ClearParentKeepTransforms(bpy.types.Operator):
    bl_idname = "myops.clear_parent_keep_transforms"
    bl_label = "Clear Parents and Keep Transforms"
    bl_description= "Clears the object parents, keeps their transforms."
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for object in selected_objects:
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            object.select_set(True)
        return {'FINISHED'}

class NormalToWorldSpace(bpy.types.Operator):
    bl_idname = "myops.normal_world_space"
    bl_label = "Change Normal Map to World Space"
    bl_description= "Changes Normal Map Shader to World Space."
    
    def execute(self, context):
        for item in bpy.data.materials:
            if item.node_tree != None:
                item.node_tree.nodes['Normal Map'].space = 'WORLD'
        return {'FINISHED'}

class NormalStrengthToHalf(bpy.types.Operator):
    bl_idname = "myops.normal_str_half"
    bl_label = "Set Normal Map Strength to 50%"
    bl_description= "Sets Normal Map Shader Strength to 50%."
    
    def execute(self, context):
        for item in bpy.data.materials:
            if item.node_tree != None:
                item.node_tree.nodes['Normal Map'].inputs[0].default_value = 0.5
        return {'FINISHED'}


class RemoveBones(bpy.types.Operator):
    bl_idname = "myops.remove_un_needed_bones"
    bl_label = "Remove unneeded bones"
    bl_description = "Removes bones that are already included in Meku Rig V7. Not for modding!"
    
    def execute(self, context):
        bones_to_remove = ["j_kao", "n_throw", "n_hijisoubi_l", "n_hijisoubi_r", "n_buki_tate_r", "n_buki_tate_l", "n_buki_l", "n_buki_r", "n_kataarmor_l", "n_kataarmor_r", "j_buki_sebo_l", "j_buki_sebo_r", "j_buki_kosi_l", "j_buki_kosi_r", "j_buki2_kosi_l", "j_buki2_kosi_r", "n_hizasoubi_l", "n_hizasoubi_r", "j_kubi", "j_kosi", "n_root", "j_asi_a_l", "j_asi_a_r", "j_asi_b_l", "j_asi_b_r", "j_asi_c_l", "j_asi_c_r", "j_asi_d_l", "j_asi_d_r", "j_asi_e_l", "j_asi_e_r", "n_hara", "j_sebo_a", "j_sebo_b", "j_sebo_c", "j_sako_l", "j_sako_r", "j_ude_a_l", "j_ude_a_r", "n_hkata_l", "n_hkata_r", "j_ude_b_l", "j_ude_b_r", "n_hhiji_l", "n_hhiji_r", "n_hte_l", "n_hte_r", "j_te_l", "j_te_r", "j_oya_a_l", "j_oya_a_r", "j_oya_b_l", "j_oya_b_r", "j_hito_a_l", "j_hito_a_r", "j_hito_b_l", "j_hito_b_r", "j_naka_a_l", "j_naka_a_r", "j_naka_b_l", "j_naka_b_r", "j_kusu_a_l", "j_kusu_a_r", "j_kusu_b_l", "j_kusu_b_r", "j_ko_a_l", "j_ko_a_r", "j_ko_b_l", "j_ko_b_r", "j_mune_l", "j_mune_r", "j_f_ulip_b", "j_f_dlip_b", "j_f_ulip_a", "j_f_dlip_a", "j_ago", "j_f_eye_l", "j_f_eye_r", "j_f_dmab_l", "j_f_dmab_r", "j_f_umab_l", "j_f_umab_r", "j_f_miken_l", "j_f_miken_r", "j_f_mayu_l", "j_f_mayu_r", "j_f_memoto", "j_f_hana", "j_f_hoho_l", "j_f_hoho_r", "j_f_lip_l", "j_f_lip_r", "j_sk_f_a_l", "j_sk_f_b_l", "j_sk_f_c_l", "j_sk_f_a_r", "j_sk_f_b_r", "j_sk_f_c_r", "j_sk_s_a_l", "j_sk_s_b_l", "j_sk_s_c_l", "j_sk_s_a_r", "j_sk_s_b_r", "j_sk_s_c_r", "j_sk_b_a_l", "j_sk_b_b_l", "j_sk_b_c_l", "j_sk_b_a_r", "j_sk_b_b_r", "j_sk_b_c_r", "n_sippo_a", "n_sippo_b", "n_sippo_c", "n_sippo_d", "n_sippo_e", "n_ear_a_r", "n_ear_b_r", "n_ear_a_l", "n_ear_b_l"]
        selected_objects = bpy.context.selected_objects
        for object in selected_objects:
            if object.type == 'ARMATURE':
                object.select_set(True)  # Select the armature object
                bpy.context.view_layer.objects.active = object  # Set the armature object to active
                bpy.ops.object.mode_set(mode='EDIT') # Set mode to Edit because it's impossible to access bones otherwise
                for bone in object.data.edit_bones:
                    if bone.name in bones_to_remove:
                        object.data.edit_bones.remove(bone)
                bpy.ops.object.mode_set(mode='OBJECT')
                object.select_set(False)
        return {'FINISHED'}

class ClearCustomSplitNormals(bpy.types.Operator):
    bl_idname = "myops.clear_split_normals"
    bl_label = "Clear Custom Split Normals"
    bl_description = "Clear custom split normals, sets Autosmooth On and to 180 degrees"
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        joined_objects = bpy.context.selected_objects
        for object in selected_objects:
            if object.type == 'MESH':
                bpy.ops.mesh.customdata_custom_splitnormals_clear() #clear custom split normals
                bpy.context.object.data.use_auto_smooth = True  # Set autosmooth to enabled
                bpy.context.object.data.auto_smooth_angle = radians(180) # Set autosmooth to 180 degrees
        return {'FINISHED'}

class MekTools_Rig_Append_Male(bpy.types.Operator):
    bl_idname = "myops.malerig"
    bl_label = "Import Rigs and Shaders"
    bl_description = "Import rig for most male bodies."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        path = os.path.dirname(__file__) + "/blends/rig.blend\\Collection\\"
        rig_name = "MaleRig"
        bpy.ops.wm.append(filename=rig_name, directory=path)
        return {"FINISHED"}

class MekTools_Rig_Append_Hroth(bpy.types.Operator):
    bl_idname = "myops.hrothgar"
    bl_label = "Import Rigs and Shaders"
    bl_description = "Import rig for Hrothgar/Roegadyn."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        path = os.path.dirname(__file__) + "/blends/rig.blend\\Collection\\"
        rig_name = "HrothRig"
        bpy.ops.wm.append(filename=rig_name, directory=path)
        return {"FINISHED"}
    
class MekTools_Rig_Append(bpy.types.Operator):
    bl_idname = "myops.femrig"
    bl_label = "Import Rigs and Shaders"
    bl_description = "Import rig for female Mid-/Highlander, Au ra and Miqo te."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        path = os.path.dirname(__file__) + "/blends/rig.blend\\Collection\\"
        rig_name = "FemaleRig"
        bpy.ops.wm.append(filename=rig_name, directory=path)
        return {"FINISHED"}

class MekTools_Rig_Append_Viera(bpy.types.Operator):
    bl_idname = "myops.viera"
    bl_label = "Import Rigs and Shaders"
    bl_description = "Import rig for Viera, Elezen and Roegadyn."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        path = os.path.dirname(__file__) + "/blends/rig.blend\\Collection\\"
        rig_name = "VieraRig"
        bpy.ops.wm.append(filename=rig_name, directory=path)
        return {"FINISHED"}

class MekTools_Rig_Append_Lala(bpy.types.Operator):
    bl_idname = "myops.lala"
    bl_label = "Import Rigs and Shaders"
    bl_description = "Import rig for Lalafel."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        path = os.path.dirname(__file__) + "/blends/rig.blend\\Collection\\"
        rig_name = "LalaRig"
        bpy.ops.wm.append(filename=rig_name, directory=path)
        return {"FINISHED"}
            
class FixMetallic(bpy.types.Operator):
    bl_idname = "myops.fixmetallic"
    bl_label = "Fix Metallic"
    bl_description = "Fixes metallic issue"
        
    def execute(self, context):
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                mat.metallic = 0
                continue
            for n in mat.node_tree.nodes:
                if n.type == 'BSDF_PRINCIPLED':
                     n.inputs["Metallic"].default_value = 0  
        return {'FINISHED'}
    
# --- Theta Functions ---

class MaterialFix(bpy.types.Operator): # Adds Custom Shader to active material
    bl_idname = "myops.matfix"
    bl_label = "Apply Custom Material Nodes"
    bl_description = "Applies Custom Material Node to objects for fixing shading issues present in FFXIV Furniture and Landscape objects"

    def execute(self, context):
        check_for_nodes()
        selected_material = bpy.context.active_object.active_material
        selected_objects = bpy.context.active_object
        change_material(selected_material)
        return {"FINISHED"}    

# --- functions for doing the things

# For nudging nodes easily
def move_node(node, x_amount, y_amount):
    node.location.x += x_amount
    node.location.y += y_amount

# For placing nodes in absolute space
def place_node(node, x_pos, y_pos):
    node.location.x = x_pos
    node.location.y = y_pos

def check_for_nodes(): #TODO: Check for all nodes? Right now this just checks for the diff-spec converter
    nodesappended = False
    for n in bpy.data.node_groups:
        if n.name == 'Diff-Spec-Converter':
            nodesappended = True
            print("Nodes Found, not appending")
    if nodesappended == False:
        append_nodegroups()
        print("Nodes not found, appending")

def append_nodegroups():
    path = os.path.dirname(__file__) + '/blends/rig.blend\\NodeTree\\'
    import_node = 'Diff-Spec-Converter'
    bpy.ops.wm.append( filename = import_node, directory = path)
    import_node2 = 'Texture-4X'
    bpy.ops.wm.append( filename = import_node2, directory = path)
    import_node3 = 'FFXIV Face Decal'
    bpy.ops.wm.append( filename = import_node3, directory = path)
    import_node4 = 'FFXIV Eye Shader'
    bpy.ops.wm.append( filename = import_node4, directory = path)
    import_node5 = 'FFXIV Skin Shader'
    bpy.ops.wm.append( filename = import_node5, directory = path)

def change_material(mat):
    print("Changing Material")
    to_remove = []
    for node in mat.node_tree.nodes:
        if node.bl_idname == 'ShaderNodeBsdfPrincipled':
            if len(node.inputs[0].links) > 0: #checking if input 0 has a connection (diffuse tex)
                checknode = node.inputs[0].links[0].from_node #assigning checknode var to that linked node
                if checknode.bl_idname != 'ShaderNodeTexImage': #if that's not an image texture, run away
                    return
                else:
                    connect_alpha(node, mat)
                    add_slap(node, mat.node_tree)
#                    if len(node.inputs[19].links) > 0:
#                        emissionNode = node.inputs.get("Emission").links[0].from_node
#                        if emissionNode.bl_idname == 'ShaderNodeTexImage':
#                            to_remove.append(emissionNode)
                    to_remove.append(node)
    for node in to_remove:
        mat.node_tree.nodes.remove(node)
    
def connect_alpha(node, mat):
    if len(node.inputs[0].links) > 0:
        if len(node.inputs[21].links) > 0:
            alphaNode = node.inputs[21].links[0].from_node
            if alphaNode.bl_idname == 'ShaderNodeTexImage':
                mat.node_tree.nodes.remove(alphaNode)
        mat.node_tree.links.new(node.inputs[0].links[0].from_node.outputs[1], node.inputs[19])

def add_slap(node, node_tree): # Relink existing materials to custom nodegroup
    #Create groupnode
    groupnode = node_tree.nodes.new('ShaderNodeGroup')
    groupnode.node_tree = bpy.data.node_groups['FFXIV Skin Shader']
    materialOut = node.outputs[0].links[0].to_node
    normalNode = node.inputs[22].links[0].from_node
    normalImage = normalNode.inputs[1].links[0].from_node    
    diffImage = node.inputs[0].links[0].from_node
    #Connect diff node to slap node
    node_tree.links.new(groupnode.inputs[2], diffImage.outputs[0])
    node_tree.links.new(groupnode.inputs[5], diffImage.outputs[1])
    node_tree.links.new(groupnode.inputs[4], normalImage.outputs[0])
    SpecExists = False
    if len(node.inputs[7].links) > 0: #Sometimes there's no spec
        SpecExists = True
        specimage = node.inputs[7].links[0].from_node
        #Connect spec node to slap node
        node_tree.links.new(groupnode.inputs[3], specimage.outputs[0])
    #Connect slap node outputs to main node inputs.
    node_tree.links.new(groupnode.outputs[0], materialOut.inputs[0])
    move_node(groupnode, -200, 250)
    move_node(diffImage, -300, 335)
    move_node(normalImage, 0, 1000)
    if SpecExists == True:
        move_node(specimage, 0, 80)
    node_tree.nodes.remove(normalNode)

def add_eyes(eyes):
    node_tree = eyes.node_tree
    for n in node_tree.nodes:
        if n.bl_idname != 'ShaderNodeOutputMaterial':
            node_tree.nodes.remove(n)
        else:
             materialOutput = n
    check_for_nodes()
    groupnode = node_tree.nodes.new('ShaderNodeGroup')
    groupnode.node_tree = bpy.data.node_groups['FFXIV Eye Shader']
    node_tree.links.new(groupnode.outputs[0], materialOutput.inputs[0])
    move_node(groupnode, 0, 357)


class EyeFix(bpy.types.Operator): # Adds Custom Shader to active material
    bl_idname = "myops.eyefix"
    bl_label = "Fix Eyes"
    bl_description = "Use this only on the iris material."

    def execute(self, context):
        selected_material = bpy.context.active_object.active_material
        add_eyes(selected_material)
        return {"FINISHED"}

class RigLayers(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rig Layers"
    bl_idname = "VIEW3D_PT_rig_layers_"
    bl_category = 'Item'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

#  This is where you can add armature layer buttons and name them for the UI
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=1, toggle=True, text='Torso')

        row = col.row()
        row.prop(context.active_object.data, 'layers', index=0, toggle=True, text='Face')
        row.prop(context.active_object.data, 'layers', index=2, toggle=True, text='Hands')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=25, toggle=True, text='IK')
        row.prop(context.active_object.data, 'layers', index=9, toggle=True, text='FK')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=7, toggle=True, text='Physics')
        row.prop(context.active_object.data, 'layers', index=16, toggle=True, text='Extra')
        
        row = col.row()
        row.prop(context.active_object.data, 'layers', index=31, toggle=True, text='Base Bones')                

        #This is for the IK FK Slider... doesnt work.. yet... send help... and pizza.
        #layout.prop(pose_bones['hand.IK.L'], '["IK_Stretch"]', text='IK Stretch', slider=True)       
              
classes = [RigLayers, EyeFix, MaterialFix, MainPanel, FixMetallic, ClearCustomSplitNormals, RiggingPanel, ChangeToAlpha, ClearParentKeepTransforms, NormalToWorldSpace, NormalStrengthToHalf, RemoveBones, MekTools_Rig_Append_Male, MekTools_Rig_Append, MekTools_Rig_Append_Viera, MekTools_Rig_Append_Lala, MekTools_Rig_Append_Hroth]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()