import pytest
from fastapi import HTTPException
from backend.services.operaciones import evaluar_expresion, calcular


class TestEvaluarExpresion:
    def test_suma_basica(self):
        assert evaluar_expresion("2+2") == "4"

    def test_sqrt(self):
        assert evaluar_expresion("sqrt(16)") == "4"

    def test_factorial(self):
        assert evaluar_expresion("factorial(5)") == "120"

    def test_potencia(self):
        assert evaluar_expresion("2^10") == "1024"

    def test_sin_cero(self):
        assert evaluar_expresion("sin(0)") == "0"

    def test_expresion_vacia(self):
        with pytest.raises(HTTPException) as exc:
            evaluar_expresion("")
        assert exc.value.status_code == 400

    def test_caracteres_invalidos(self):
        with pytest.raises(HTTPException) as exc:
            evaluar_expresion("2 + 2; print(1)")
        assert exc.value.status_code == 400


class TestSeguridad:
    @pytest.mark.parametrize("expr", [
        "__import__('os')",
        "exec('x=1')",
        "os.system('ls')",
        "__builtins__",
        "globals()",
    ])
    def test_expresiones_peligrosas_bloqueadas(self, expr):
        with pytest.raises(HTTPException) as exc:
            evaluar_expresion(expr)
        assert exc.value.status_code == 400


class TestCalcular:
    def test_dividir(self):
        assert calcular(10, 2, "dividir") == 5.0

    def test_sumar(self):
        assert calcular(3, 3, "sumar") == 6

    def test_restar(self):
        assert calcular(10, 4, "restar") == 6

    def test_multiplicar(self):
        assert calcular(3, 4, "multiplicar") == 12

    def test_division_por_cero(self):
        with pytest.raises(HTTPException) as exc:
            calcular(5, 0, "dividir")
        assert exc.value.status_code == 400

    def test_operacion_invalida(self):
        with pytest.raises(HTTPException) as exc:
            calcular(1, 1, "potencia")
        assert exc.value.status_code == 400
