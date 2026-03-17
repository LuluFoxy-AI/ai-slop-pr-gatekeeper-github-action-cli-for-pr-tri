import runpy
import builtins
import pytest
from unittest import mock

import pr_ai_sentinel as script_under_test


def test_main_exists_and_callable():
    assert hasattr(script_under_test, "main")
    assert callable(script_under_test.main)


def test_main_accepts_none_and_various_sequences(monkeypatch):
    # Patch print to avoid noisy output during the test
    with mock.patch("builtins.print") as mock_print:
        assert script_under_test.main(None) == 0
        assert script_under_test.main([]) == 0
        assert script_under_test.main(["one", "two"]) == 0
        # ensure print was called at least once by the function
        mock_print.assert_called()


def test_main_prints_hello_and_returns_zero(capsys):
    ret = script_under_test.main([])
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out == "hello\n"


def test_main_with_tuple_args_returns_zero_and_prints(capsys):
    ret = script_under_test.main(("arg1", "arg2"))
    captured = capsys.readouterr()
    assert ret == 0
    assert captured.out.strip() == "hello"


def test_running_module_as_script_raises_systemexit_with_code_zero():
    # When run as __main__, the module should raise SystemExit(main())
    with mock.patch("builtins.print"):
        with pytest.raises(SystemExit) as excinfo:
            runpy.run_module("pr_ai_sentinel", run_name="__main__")
    # SystemExit should carry the return value from main (0)
    assert excinfo.value.code == 0


def test_print_exception_propagates():
    # If print (an external call) raises, that exception should propagate from main
    with mock.patch("builtins.print", side_effect=RuntimeError("print failed")):
        with pytest.raises(RuntimeError, match="print failed"):
            script_under_test.main([])