import inspect
import logging
import os
import sys


def _dummy_trace_function(value):
    return ""


def _get_frame_function_name_with_string(depth: int):
    return f"[{sys._getframe(depth).f_code.co_name}]"


class TraceLogger:

    def __init__(self, prefix: str = None, trace_class: bool = True, trace_function: bool = True):
        op_env = os.getenv("OP_ENV") or "dev"
        # custom prefix 를 사용하지 않고 trace_class 를 사용할 때, 로거의 prefix 는 호출한 클래스 이름이 됨.
        if prefix is None and trace_class is True:
            caller_frame = sys._getframe(1)
            caller_classname = TraceLogger._get_classname(caller_frame)
            caller_function_name = caller_frame.f_code.co_name
            prefix = f"[{caller_classname or caller_function_name}]"
        # custom prefix 를 사용하고 trace_class 를 사용할 때, 로거의 prefix 는 'custom_prefix-trace_class 가 됨'
        elif prefix is not None and trace_class is True:
            caller_frame = sys._getframe(1)
            caller_classname = TraceLogger._get_classname(caller_frame)
            caller_function_name = caller_frame.f_code.co_name
            prefix = f"[{prefix}-{caller_classname}]" or f"[{prefix}-{caller_function_name}]"
        # custom prefix 와 trace_class 를 둘 다 사용하지 않을 때
        elif prefix is None and trace_class is False:
            pass

        self._logger = logging.getLogger(prefix)
        if op_env in ["prod", "dev"]:
            self._prefix = prefix
        else:
            self._prefix = ""

        if trace_function:
            self._trace_function = _get_frame_function_name_with_string
        else:
            self._trace_function = _dummy_trace_function

    @staticmethod
    def _get_classname(frame):
        args, _, _, value_dict = inspect.getargvalues(frame)
        # we check the first parameter for the frame function is
        # named 'self'
        if len(args) and args[0] == 'self':
            # in that case, 'self' will be referenced in value_dict
            instance = value_dict.get('self', None)
            if instance:
                # return its class
                return getattr(instance, '__class__', None).__name__
        # return None otherwise
        return None

    def _make_log(self, msg: object):
        caller = self._trace_function(3)
        return f"{self._prefix}{caller} " + msg

    def info(self, msg: object) -> None:
        self._logger.info(self._make_log(msg))

    def warning(self, msg: object) -> None:
        self._logger.warning(self._make_log(msg))

    def error(self, msg: object) -> None:
        self._logger.error(self._make_log(msg))

    def debug(self, msg: object) -> None:
        self._logger.debug(self._make_log(msg))



if __name__ == "__main__":

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logging.basicConfig()
    test = TraceLogger(prefix="test", trace_class=True, trace_function=True)
    test.info("Test")
    def test2(log: TraceLogger):
        log.info("omg")
    test2(test)