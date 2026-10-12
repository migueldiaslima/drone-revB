# -*- coding: ascii -*-
"""s06_render.py - offscreen VTK renderer for CadQuery solids (flat shading, feature edges). ASCII only."""
import vtk


def to_polydata(wp, tol=0.05):
    shapes = wp.vals() if hasattr(wp, "vals") else [wp]
    app = vtk.vtkAppendPolyData()
    for s in shapes:
        v, t = s.tessellate(tol, 0.2)
        pts = vtk.vtkPoints()
        for p in v:
            pts.InsertNextPoint(p.x, p.y, p.z)
        cells = vtk.vtkCellArray()
        for tri in t:
            cells.InsertNextCell(3)
            for i in tri:
                cells.InsertCellPoint(i)
        pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells)
        app.AddInputData(pd)
    app.Update()
    clean = vtk.vtkCleanPolyData(); clean.SetInputConnection(app.GetOutputPort()); clean.Update()
    return clean.GetOutput()


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def render(items, fname, view=(1, -1, 0.8), up=(0, 0, 1), size=(900, 700), zoom=1.0, focal=None, scale=None):
    """items: list of (workplane, colour hex, opacity)."""
    ren = vtk.vtkRenderer(); ren.SetBackground(1, 1, 1)
    ren.SetUseDepthPeeling(1); ren.SetMaximumNumberOfPeels(8)
    win = vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.AddRenderer(ren); win.SetSize(*size)
    win.SetAlphaBitPlanes(1); win.SetMultiSamples(0)
    for wp, col, op in items:
        pd = to_polydata(wp)
        nrm = vtk.vtkPolyDataNormals(); nrm.SetInputData(pd); nrm.SetFeatureAngle(35); nrm.SplittingOn(); nrm.Update()
        m = vtk.vtkPolyDataMapper(); m.SetInputConnection(nrm.GetOutputPort())
        a = vtk.vtkActor(); a.SetMapper(m)
        pr = a.GetProperty(); pr.SetColor(*hexrgb(col)); pr.SetOpacity(op)
        pr.SetAmbient(0.45); pr.SetDiffuse(0.7); pr.SetSpecular(0.05)
        ren.AddActor(a)
        fe = vtk.vtkFeatureEdges(); fe.SetInputData(pd); fe.BoundaryEdgesOn(); fe.FeatureEdgesOn()
        fe.SetFeatureAngle(35); fe.ManifoldEdgesOff(); fe.NonManifoldEdgesOff(); fe.ColoringOff()
        em = vtk.vtkPolyDataMapper(); em.SetInputConnection(fe.GetOutputPort())
        ea = vtk.vtkActor(); ea.SetMapper(em); ea.GetProperty().SetColor(0.15, 0.15, 0.15)
        ea.GetProperty().SetLineWidth(1.2); ea.GetProperty().SetOpacity(min(1.0, op + 0.2))
        ren.AddActor(ea)
    cam = ren.GetActiveCamera(); cam.ParallelProjectionOn()
    ren.ResetCamera()
    f = focal if focal else cam.GetFocalPoint()
    d = 500.0
    cam.SetFocalPoint(*f)
    cam.SetPosition(f[0] + view[0] * d, f[1] + view[1] * d, f[2] + view[2] * d)
    cam.SetViewUp(*up)
    ren.ResetCamera()
    if focal:
        cam.SetFocalPoint(*f)
        cam.SetPosition(f[0] + view[0] * d, f[1] + view[1] * d, f[2] + view[2] * d)
    if scale:
        cam.SetParallelScale(scale)
    else:
        cam.Zoom(zoom)
    ren.ResetCameraClippingRange()
    light = vtk.vtkLight(); light.SetLightTypeToCameraLight(); light.SetPosition(0.4, 0.8, 1); light.SetIntensity(0.9)
    ren.AddLight(light)
    l2 = vtk.vtkLight(); l2.SetLightTypeToCameraLight(); l2.SetPosition(-0.6, -0.3, 1); l2.SetIntensity(0.45); ren.AddLight(l2)
    win.Render()
    w2i = vtk.vtkWindowToImageFilter(); w2i.SetInput(win); w2i.Update()
    wr = vtk.vtkPNGWriter(); wr.SetFileName(fname); wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()
