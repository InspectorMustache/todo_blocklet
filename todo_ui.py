import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class TodoWindow(Gtk.Window):

    def __init__(self, task_dict):
        Gtk.Window.__init__(self, title='Todo.txt')
        self.set_border_width(10)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.grid = Gtk.Grid(column_spacing=5, row_spacing=4)
        self.add(self.grid)

        screen = self.get_screen()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('todo_markup.css')
        Gtk.StyleContext.\
            add_provider_for_screen(screen,
                                    css_provider,
                                    Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.populate_listbox(task_dict)

        separator = Gtk.Separator()
        exit_button = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        self.grid.attach_next_to(separator, None, Gtk.PositionType.BOTTOM, 3, 1)
        self.grid.attach_next_to(exit_button, separator, Gtk.PositionType.BOTTOM, 3, 1)

        self.connect('delete-event', Gtk.main_quit)
        exit_button.connect('clicked', self.clicked_ok)

    def populate_listbox(self, task_dict):
        categories = list(task_dict)
        categories.sort()
        pos = 0
        for cat in categories:
            self.populate_category(task_dict[cat], cat, pos)
            pos += len(task_dict[cat])

    def populate_category(self, task_list, category, pos):
        for index, task in enumerate(task_list):
            label = self.create_list_entry(task, category)
            self.grid.attach(label, 0, index + pos, 1, 1)

            done_button = Gtk.Button.new_from_icon_name('emblem-ok-symbolic',
                                                        Gtk.IconSize.BUTTON)
            done_button.pressed = False
            done_button.connect('clicked', self.clicked_done,
                                label, category, task)

            rm_button = Gtk.Button.new_from_icon_name('edit-delete-symbolic',
                                                      Gtk.IconSize.BUTTON)
            rm_button.pressed = False
            rm_button.connect('clicked', self.clicked_rm,
                               label, category)

            self.grid.attach_next_to(done_button, label,
                                     Gtk.PositionType.RIGHT,
                                     1, 1)
            self.grid.attach_next_to(rm_button, done_button,
                                     Gtk.PositionType.RIGHT,
                                     1, 1)

    def create_list_entry(self, task, css_class):
        label = Gtk.Label(task)
        label.get_style_context().add_class(css_class)
        label.set_alignment(0, .5)
        return label

    def clicked_done(self, button, label, category, task):
        if button.pressed == False:
            self.remove_css_classes(label)
            label.get_style_context().add_class('done')
            label.props.label = "✓ {}".format(task)
            button.pressed = True
        else:
            self.remove_css_classes(label)
            label.get_style_context().add_class(category)
            label.props.label = task
            button.pressed = False

    def clicked_rm(self, button, label, category):
        if button.pressed == False:
            self.remove_css_classes(label)
            label.get_style_context().add_class('removed')
            button.pressed = True
        else:
            self.remove_css_classes(label)
            label.get_style_context().add_class(category)
            button.pressed = False

    def clicked_ok(self, button):
        Gtk.main_quit()

    def remove_css_classes(self, widget):
        context = widget.get_style_context()
        classes = context.list_classes()
        for css_class in classes:
            context.remove_class(css_class)


def gui_from_tasks(task_dict):
    win = TodoWindow(task_dict)
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
