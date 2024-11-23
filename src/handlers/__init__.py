from .start import router as start_router
from .statistics import router as stats_router

from .base.flashcard import router as flash_router
from .base.exam import router as exam_router
from .base.math import router as math_router

from .flash.flash_theory import router as flash_theory_router
from .flash.flash_formula import router as flash_formula_router
from .flash.flash_instrument import router as flash_instrument_router

from .exams.exam_theory import router as exam_theory_router
from .exams.exam_formula import router as exam_formula_router
from .exams.exam_instrument import router as exam_instrument_router
