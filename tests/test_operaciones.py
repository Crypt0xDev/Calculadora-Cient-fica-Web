import pytest
from fastapi import HTTPException
from backend.services.operaciones import evaluar_expresion, calcular


class TestAritmetica:
    def test_suma(self):
        assert evaluar_expresion("5+3") == "8"

    def test_resta(self):
        assert evaluar_expresion("10-4") == "6"

    def test_multiplicacion(self):
        assert evaluar_expresion("6*7") == "42"

    def test_division(self):
        assert evaluar_expresion("10/4") == "2.5"

    def test_potencia(self):
        assert evaluar_expresion("2^10") == "1024"

    def test_negativo(self):
        assert evaluar_expresion("-5+10") == "5"


class TestRaicesYPotencias:
    def test_sqrt_exacto(self):
        assert evaluar_expresion("sqrt(16)") == "4"

    def test_sqrt_decimal(self):
        assert evaluar_expresion("sqrt(2)") == "1.4142135624"

    def test_cuadrado(self):
        assert evaluar_expresion("7^2") == "49"

    def test_10_potencia(self):
        assert evaluar_expresion("10^3") == "1000"

    def test_inverso(self):
        assert evaluar_expresion("1/5") == "0.2"


class TestTrigonometriaDEG:
    """El frontend envía sind/cosd/tand cuando el modo es DEG."""

    def test_sin_0(self):
        assert evaluar_expresion("sind(0)") == "0"

    def test_sin_30(self):
        assert evaluar_expresion("sind(30)") == "0.5"

    def test_sin_90(self):
        assert evaluar_expresion("sind(90)") == "1"

    def test_cos_0(self):
        assert evaluar_expresion("cosd(0)") == "1"

    def test_cos_60(self):
        assert evaluar_expresion("cosd(60)") == "0.5"

    def test_cos_90(self):
        r = float(evaluar_expresion("cosd(90)"))
        assert abs(r) < 1e-9

    def test_tan_45(self):
        assert evaluar_expresion("tand(45)") == "1"

    def test_tan_0(self):
        assert evaluar_expresion("tand(0)") == "0"


class TestTrigonometriaRAD:
    def test_sin_pi(self):
        assert evaluar_expresion("sin(pi)") == "0"

    def test_cos_pi(self):
        assert evaluar_expresion("cos(pi)") == "-1"

    def test_asin(self):
        assert evaluar_expresion("asin(1)") == "1.5707963268"

    def test_acos(self):
        assert evaluar_expresion("acos(1)") == "0"

    def test_atan(self):
        assert evaluar_expresion("atan(1)") == "0.7853981634"


class TestInversaTrigDEG:
    """El frontend envía asind/acosd/atand en modo DEG; el resultado debe estar en grados."""

    def test_acosd_05(self):
        assert evaluar_expresion("acosd(0.5)") == "60"

    def test_asind_05(self):
        assert evaluar_expresion("asind(0.5)") == "30"

    def test_atand_1(self):
        assert evaluar_expresion("atand(1)") == "45"

    def test_acosd_1(self):
        assert evaluar_expresion("acosd(1)") == "0"

    def test_acosd_0(self):
        assert evaluar_expresion("acosd(0)") == "90"

    def test_asind_1(self):
        assert evaluar_expresion("asind(1)") == "90"

    def test_acosd_fuera_de_dominio(self):
        """acosd(55) debe fallar con 400 — fuera del dominio [-1, 1]."""
        with pytest.raises(HTTPException) as exc:
            evaluar_expresion("acosd(55)")
        assert exc.value.status_code == 400


class TestLogaritmos:
    def test_log_100(self):
        assert evaluar_expresion("log(100)") == "2"

    def test_log_1000(self):
        assert evaluar_expresion("log(1000)") == "3"

    def test_ln_e(self):
        assert evaluar_expresion("ln(e)") == "1"

    def test_exp_1(self):
        assert evaluar_expresion("exp(1)") == "2.7182818285"


class TestOtrasFunciones:
    def test_abs(self):
        assert evaluar_expresion("abs(-9)") == "9"

    def test_factorial_6(self):
        assert evaluar_expresion("factorial(6)") == "720"

    def test_factorial_0(self):
        assert evaluar_expresion("factorial(0)") == "1"

    def test_floor(self):
        assert evaluar_expresion("floor(3.9)") == "3"

    def test_ceil(self):
        assert evaluar_expresion("ceil(3.1)") == "4"

    def test_pi(self):
        assert evaluar_expresion("pi") == "3.1415926536"

    def test_e(self):
        assert evaluar_expresion("e") == "2.7182818285"


class TestExpresionesComplejas:
    def test_sind_mas_sqrt(self):
        assert evaluar_expresion("sind(30)+sqrt(16)") == "4.5"

    def test_potencia_mas_factorial(self):
        assert evaluar_expresion("2^8+factorial(3)") == "262"

    def test_cosd_multiplicado(self):
        assert evaluar_expresion("cosd(60)*2") == "1"


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

    def test_cos_no_bloqueado_por_os(self):
        """cos(pi) no debe bloquearse por contener 'os'."""
        assert evaluar_expresion("cos(pi)") == "-1"

    def test_acos_no_bloqueado_por_os(self):
        """acos(1) no debe bloquearse por contener 'os'."""
        assert evaluar_expresion("acos(1)") == "0"

    def test_expresion_vacia(self):
        with pytest.raises(HTTPException) as exc:
            evaluar_expresion("")
        assert exc.value.status_code == 400

    def test_caracteres_invalidos(self):
        with pytest.raises(HTTPException) as exc:
            evaluar_expresion("2 + 2; print(1)")
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

