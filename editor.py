import subprocess

import wx
from wx.lib.splitter import MultiSplitterWindow
from wx.lib.dialogs import ScrolledMessageDialog


class Frame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, title='Editor',
                      pos=(150, 150), size=(800, 600))
    self.Bind(wx.EVT_CLOSE, self.OnClose)

    self.main_panel = Editor(self)
    self.main_sizer = wx.BoxSizer()

    self.main_sizer.Add(self.main_panel, 1, wx.EXPAND|wx.ALL)

    # self.main_sizer.Add(wx.Button(self, 1, 'Main'), wx.EXPAND|wx.ALL)
    # self.main_sizer.Add(wx.Button(self, 1, 'One'), wx.EXPAND|wx.ALL)

    self.SetSizer(self.main_sizer)
    self.Maximize()
    # self.Center()
    self.Layout()


  def OnClose(self, event):
    self.Destroy()


class Editor(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent, wx.EXPAND|wx.ALL)

    self.main_splitter = MultiSplitterWindow(
      self, style=wx.SP_LIVE_UPDATE)
    self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

    self.left_panel = LeftPanel(self.main_splitter)
    self.right_panel = RightPanel(self.main_splitter)

    self.main_splitter.AppendWindow(self.left_panel, self.Parent.GetSize()[1])
    self.main_splitter.AppendWindow(self.right_panel, self.Parent.GetSize()[1])
    self.main_splitter.SetSashPosition(1, True)
    self.main_splitter.SizeWindows()

    self.main_sizer.Add(self.main_splitter, 1, wx.EXPAND|wx.ALL)

    self.SetSizer(self.main_sizer)
    self.Layout()


class EditorPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    self.file_name = ''
    self.main_sizer = wx.BoxSizer(wx.VERTICAL)

    self.text_ctrl = wx.TextCtrl(
      self, -1, 'DEFAULT', # size=(200, 100),
      style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)

    self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

    self.main_sizer.Add(self.text_ctrl, 1, wx.EXPAND|wx.ALL)
    self.main_sizer.Add(self.button_sizer, 0, wx.EXPAND|wx.ALL)

    self.SetSizer(self.main_sizer)
    self.Layout()

  def read_file(self, file_name):
    self.text_ctrl.Clear()
    f = open(file_name, 'r')
    for line in f:
      self.text_ctrl.AppendText(line)
    f.close()

  def OnSave(self, event):
    self.text_ctrl.SaveFile(self.file_name)
    event.Skip()

  def OnRun(self, event):
    # output = subprocess.check_output(['echo', self.file_name])
    output = subprocess.check_output(['./test.sh', self.file_name])
    dialog = ScrolledMessageDialog(self, msg=output, caption='Output',
                                   size=self.Parent.GetSize())
    # style=wx.MAXIMIZE)
    dialog.ShowModal()


class LeftPanel(EditorPanel):
  def __init__(self, parent):
    EditorPanel.__init__(self, parent)

    self.text_ctrl.SetBackgroundColour(wx.Colour(0, 255, 0))
    self.text_ctrl.SetForegroundColour(wx.Colour(0, 0, 0))

    self.save_button = wx.Button(self, 1, 'Save &Pos')
    self.save_button.SetBackgroundColour(wx.Colour(80, 80, 80))
    self.save_button.SetForegroundColour(wx.Colour(255, 225, 255))
    self.run_button = wx.Button(self, 1, 'Run P&os')
    self.run_button.SetBackgroundColour(wx.Colour(80, 80, 80))
    self.run_button.SetForegroundColour(wx.Colour(255, 255, 255))

    self.save_button.Bind(wx.EVT_BUTTON, self.OnSave , self.save_button)
    self.run_button.Bind(wx.EVT_BUTTON, self.OnRun , self.run_button)

    self.button_sizer.Add(self.save_button, 0, wx.EXPAND)
    self.button_sizer.Add(self.run_button, 0, wx.EXPAND)

    self.file_name = 'testListPos'
    self.read_file(self.file_name)

    self.Layout()


class RightPanel(EditorPanel):
  def __init__(self, parent):
    EditorPanel.__init__(self, parent)

    self.text_ctrl.SetBackgroundColour(wx.Colour(255, 0, 0))
    self.text_ctrl.SetForegroundColour(wx.Colour(255, 255, 255))

    self.save_button = wx.Button(self, 1, 'Save &Neg')
    self.save_button.SetBackgroundColour(wx.Colour(80, 80, 80))
    self.save_button.SetForegroundColour(wx.Colour(255, 225, 255))
    self.run_button = wx.Button(self, 1, 'Run N&eg')
    self.run_button.SetBackgroundColour(wx.Colour(80, 80, 80))
    self.run_button.SetForegroundColour(wx.Colour(255, 255, 255))

    self.save_button.Bind(wx.EVT_BUTTON, self.OnSave , self.save_button)
    self.run_button.Bind(wx.EVT_BUTTON, self.OnRun , self.run_button)

    self.button_sizer.Add(self.save_button, 0, wx.EXPAND)
    self.button_sizer.Add(self.run_button, 0, wx.EXPAND)

    self.file_name = 'testListNeg'
    self.read_file(self.file_name)

    self.Layout()


if __name__ == '__main__':
  app = wx.App(False)
  frame = Frame()
  frame.Show(True)
  app.MainLoop()
