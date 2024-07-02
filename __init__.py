import bpy
import os
import time, datetime

class PrefixSavePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    prefix : bpy.props.StringProperty(name="Prefix calculation",
                    description="Python string that calculates the file prefix",
                    default="timestamp().strftime('%Y_%m_%d_%H_%M_%S') + '_'")

    copies : bpy.props.BoolProperty(name="Save as copies",
                    description="Save prefixed copies instead of renaming the existing file",
                    default=True)

    backupFolder : bpy.props.StringProperty(name="Backup folder name",
                description="The exact name of the folder where backups will be saved in",
                default="backup")

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        row = col.row()
        row.prop(self,"copies")
        row = col.row()
        row.prop(self,"prefix")
        row = col.row()
        row.prop(self,"backupFolder")

def timestamp():
    # convienience function that is available to the user in their calculations
    return datetime.datetime.fromtimestamp(time.time())

class PrefixFileSave(bpy.types.Operator):
    """Set a filename prefix before saving the file"""
    bl_idname = "wm.save_prefix"
    bl_label = "Save Backup"

    def execute(self, context):
        user_preferences = context.preferences
        addon_prefs = user_preferences.addons[__package__].preferences
        outname = eval(addon_prefs.prefix) + bpy.path.basename(bpy.data.filepath)
        outpath = os.path.join(os.path.dirname(bpy.path.abspath(bpy.data.filepath)), addon_prefs.backupFolder)
        print(os.path.join(outpath, outname))

        # If no /backup folder exists, create one
        if not(os.path.exists(outpath)):
            os.mkdir(outpath)

        #print(os.path.join(outpath, outname))
        if addon_prefs.copies:
            return bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outpath, outname),
                    check_existing=True, copy=True)
        return bpy.ops.wm.save_mainfile(filepath=os.path.join(outpath, outname),
                    check_existing=True)

def menu_save_prefix(self, context):
    self.layout.operator(PrefixFileSave.bl_idname, text=PrefixFileSave.bl_label, icon="FILE_TICK")

def register():
    bpy.utils.register_class(PrefixSavePreferences)
    bpy.utils.register_class(PrefixFileSave)

    # add the menuitem to the top of the file menu
    bpy.types.TOPBAR_MT_file.prepend(menu_save_prefix)

    wm = bpy.context.window_manager
    win_keymaps = wm.keyconfigs.user.keymaps.get('Window')
    if win_keymaps:
        # disable standard save file keymaps


        # add a keymap for our save operator
        pass


def unregister():

    wm = bpy.context.window_manager
    win_keymaps = wm.keyconfigs.user.keymaps.get('Window')
    if win_keymaps:
    	pass

    bpy.types.TOPBAR_MT_file.remove(menu_save_prefix)

    bpy.utils.unregister_class(PrefixFileSave)
    bpy.utils.unregister_class(PrefixSavePreferences)

if __package__ == "__main__":
    register()