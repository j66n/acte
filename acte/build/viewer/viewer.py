from __future__ import annotations

from acte.build.viewer.button_viewer import ButtonViewer
from acte.build.viewer.cache_viewer import CacheViewer
from acte.build.viewer.component_viewer import ComponentViewer
from acte.build.viewer.div_viewer import DivViewer
from acte.build.viewer.dyna_viewer import DynaViewer
from acte.build.viewer.input_viewer import InputViewer
from acte.build.viewer.text_viewer import TextViewer


class Viewer(
    DivViewer,
    TextViewer,
    ButtonViewer,
    InputViewer,

    ComponentViewer,
    DynaViewer,
    CacheViewer,
):
    pass
