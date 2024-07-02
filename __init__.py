import bpy
import os
import time, datetime

class PrefixSavePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Preferences setting to configure the backup folder name 
    backupFolder : bpy.props.StringProperty(name="Backup folder name",
                description="The name of the folder where backups will be saved in",
                default="backup")
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row()
        row.prop(self,"backupFolder")

def timestamp():
    # convienience function that is available to the user in their calculations
    return datetime.datetime.fromtimestamp(time.time())

class PrefixFileSave(bpy.types.Operator):
    """Create a file backup"""
    bl_idname = "wm.save_prefix"
    bl_label = "Save Backup"

    def execute(self, context):
        user_preferences = context.preferences
        addon_prefs = user_preferences.addons[__package__].preferences
        prefix = "timestamp().strftime('%Y_%m_%d_%H_%M_%S') + '_'"

        outname = eval(prefix) + bpy.path.basename(bpy.data.filepath)
        outpath = os.path.join(os.path.dirname(bpy.path.abspath(bpy.data.filepath)), addon_prefs.backupFolder)
        print(os.path.join(outpath, outname))

        # If no /backup folder exists, create one
        if not(os.path.exists(outpath)):
            os.mkdir(outpath)

        return bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outpath, outname), check_existing=True, copy=True)


def menu_save_prefix(self, context):
    self.layout.operator(PrefixFileSave.bl_idname, text=PrefixFileSave.bl_label, icon="FILE_TICK")

def register():
    bpy.utils.register_class(PrefixSavePreferences)
    bpy.utils.register_class(PrefixFileSave)
    bpy.types.TOPBAR_MT_file.prepend(menu_save_prefix)

def unregister():
    bpy.utils.unregister_class(PrefixFileSave)
    bpy.utils.unregister_class(PrefixSavePreferences)
    bpy.types.TOPBAR_MT_file.remove(menu_save_prefix)

if __package__ == "__main__":
    register()