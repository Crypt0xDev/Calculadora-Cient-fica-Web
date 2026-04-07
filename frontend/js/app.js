// =============================================================
// Archivo  : frontend/js/app.js
// Autor    : Alexis Noe Gonzales Perez
// Proyecto : Calculadora Científica Web
// Desc.    : Controla todo el comportamiento de la calculadora
//            en el navegador. Maneja los botones, construye la
//            expresión matemática y la envía a la API del backend.
// =============================================================


// ── VARIABLES DE ESTADO ─────────────────────────────────────────
// Estas variables guardan el "estado" actual de la calculadora.
// El estado es toda la información que necesita recordar mientras funciona.

let expr     = '';       // La expresión que se está construyendo (ej: "sin(30)+2^8")
let result   = '0';      // El último resultado calculado (para encadenar operaciones)
let memory   = 0;        // Valor guardado en memoria con M+/M-
let ans      = 0;        // ANS: guarda el resultado para reutizarlo con el botón ANS
let isDeg    = true;     // Modo angular: true = grados (DEG), false = radianes (RAD)
let justCalc = false;    // true si se acaba de presionar "=", para manejar el siguiente input

// Tabla de conversión: símbolo visual → texto que entiende Python
// El display muestra × pero Python necesita *, etc.
const DISPLAY_TO_API = { '×': '*', '÷': '/', '−': '-', 'π': 'pi', 'e': 'e' };


// ── VISTA PREVIA EN TIEMPO REAL (sin presionar =) ───────────────
// Usamos "debounce": esperamos 400ms de inactividad antes de llamar la API,
// para no enviar una petición por cada tecla pulsada.
let previewTimer = null;

/**
 * Calcula el resultado de la expresión actual y lo muestra en #preview-display.
 * Se llama automáticamente tras cada pulsación de tecla.
 * No modifica nada si la expresión está vacía o termina con un operador.
 */
async function computePreview() {
  clearTimeout(previewTimer);
  const previewEl = document.getElementById('preview-display');

  // Criterios para NO calcular (expresión incompleta o vacía)
  const trimmed = (expr || '').trim();
  if (!trimmed
      || /[\+\-\×\÷\^\(\,]$/.test(trimmed)
      || trimmed.length < 2) {
    previewEl.textContent = '';
    return;
  }

  // Esperar 400ms antes de enviar la petición (evitar spam a la API)
  previewTimer = setTimeout(async () => {
    try {
      // Convertir símbolos visuales al formato que entiende Python
      let apiExpr = expr;
      for (const [sym, rep] of Object.entries(DISPLAY_TO_API)) {
        apiExpr = apiExpr.split(sym).join(rep);
      }
      if (isDeg) {
        apiExpr = apiExpr.replace(/\b(sin|cos|tan)\(/g, '$1d(');
      }
      const res = await fetch('/api/calcular/expresion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expresion: apiExpr }),
      });
      if (res.ok) {
        const data = await res.json();
        previewEl.textContent = '= ' + data.resultado;  // Mostrar "= 42"
      } else {
        previewEl.textContent = '';  // Expresión aún incompleta, no mostrar error
      }
    } catch {
      previewEl.textContent = '';  // Sin conexión
    }
  }, 400);
}


// ── FUNCIONES DE PANTALLA ────────────────────────────────────────

/**
 * Actualiza los tres elementos del display:
 * - expression-display: la expresión que el usuario está escribiendo
 * - main-display: el valor principal (el que se ve grande)
 * - error-display: mensajes de error (vacío cuando todo está bien)
 */
function updateDisplay(val) {
  // Si se pasa un valor explícito, mostrarlo; si no, mostrar la expresión o "0"
  document.getElementById('main-display').textContent = val || expr || '0';
  document.getElementById('expression-display').textContent = expr;
  document.getElementById('error-display').textContent = '';  // Limpiar errores anteriores
}

/**
 * Muestra un error en la pantalla: pone "Error" en el display grande
 * y el mensaje descriptivo en el display pequeño de abajo.
 */
function showError(msg) {
  document.getElementById('main-display').textContent = 'Error';
  document.getElementById('error-display').textContent = msg;
}


// ── INSERTAR TEXTO EN LA EXPRESIÓN ──────────────────────────────

/**
 * Agrega un carácter a la expresión (dígito, operador, paréntesis, punto).
 * Maneja el caso especial de cuando se acaba de calcular con "=".
 */
function insertTxt(ch) {
  // Si el usuario acaba de presionar "=" y ahora presiona un número,
  // empezamos una nueva expresión desde cero
  if (justCalc && /[\d\.]/.test(ch)) {
    expr = '';
  }
  // Si el usuario acaba de calcular y presiona un operador,
  // encadenamos desde el resultado anterior (ej: 5 → + → sigue desde 5)
  if (justCalc && /[+\-×÷\^]/.test(ch)) {
    expr = result;
  }
  justCalc = false;  // Ya no estamos en "modo resultado"
  expr += ch;        // Agregamos el carácter a la expresión
  updateDisplay();
  computePreview();  // Actualizar la vista previa en tiempo real
}

/**
 * Inserta una función matemática en la expresión.
 *
 * Operadores SUFIJO (x², x⁻¹, x^y): envuelven toda la expresión actual
 * entre paréntesis y aplican el exponente. Ejemplo:
 *   expr = "5+3"  →  presionar x²  →  expr = "(5+3)^2"  = 64
 *
 * Funciones PREFIJO (sin(, cos(, sqrt(, etc.): se agregan al final y
 * el usuario escribe el argumento dentro de los paréntesis.
 */
function insertFn(fn) {
  const wasJustCalc = justCalc;  // Guardar estado antes de resetearlo
  justCalc = false;

  // ANS: insertar el último resultado calculado (como constante)
  if (fn === 'ans') {
    expr += ans;
    updateDisplay();
    computePreview();
    return;
  }

  // ── Operadores sufijo ───────────────────────────────────────
  // La base es: el resultado anterior (si recién calculamos) o la expr actual
  const base = wasJustCalc ? result : (expr || '0');

  // x² — elevar al cuadrado toda la expresión actual
  if (fn === '^2') {
    expr = `(${base})^2`;
    updateDisplay();
    computePreview();
    return;
  }

  // x⁻¹ — inverso multiplicativo de la expresión actual
  if (fn === '^(-1)') {
    expr = `(${base})^(-1)`;
    updateDisplay();
    computePreview();
    return;
  }

  // x^y — el usuario escribe el exponente DESPUÉS de presionar este botón
  // Ej: escribe "2", presiona x^y → "(2)^", escribe "10" → "(2)^10" = 1024
  if (fn === '^') {
    expr = `(${base})^`;
    updateDisplay();
    return;  // Sin preview aún (falta el exponente)
  }

  // 10^x — potencia de 10 como prefijo numérico
  if (fn === '10^') {
    expr += '10^';
    updateDisplay();
    return;
  }

  // ── Funciones prefijo (sin(, cos(, sqrt(, log(, etc.) ──────
  if (wasJustCalc && fn.endsWith('(')) {
    // Si se acaba de calcular, aplicar la función al resultado anterior
    // Ej: resultado = 16, presionar √ → sqrt(16)
    expr = fn + result + ')';
  } else {
    expr += fn;  // Simplemente agregar la función con su paréntesis
  }
  updateDisplay();
  computePreview();
}

/** Inserta el símbolo π (pi) en la expresión. */
function insertPi() {
  justCalc = false;
  expr += 'π';
  updateDisplay();
  computePreview();
}


// ── BORRAR ───────────────────────────────────────────────────────

/** Borra el último carácter de la expresión (como la tecla ⌫ del teclado). */
function backspace() {
  justCalc = false;
  expr = expr.slice(0, -1);  // slice(0, -1) elimina el último carácter
  updateDisplay();
  computePreview();
}

/** CE (Clear Entry): borra la expresión actual pero mantiene el historial. */
function clearEntry() {
  expr = '';
  updateDisplay('0');
  document.getElementById('preview-display').textContent = '';
}

/** AC (All Clear): reinicia completamente la calculadora a su estado inicial. */
function allClear() {
  expr = ''; result = '0'; justCalc = false;
  clearTimeout(previewTimer);
  document.getElementById('main-display').textContent = '0';
  document.getElementById('expression-display').textContent = '';
  document.getElementById('preview-display').textContent = '';
  document.getElementById('error-display').textContent = '';
}


// ── MODIFICADORES ────────────────────────────────────────────────

/** Cambia el signo de la expresión actual (positivo → negativo y viceversa). */
function toggleSign() {
  if (!expr) return;
  // Si ya está negativo (envuelto en -(  )), quitamos el negativo
  if (expr.startsWith('-(') && expr.endsWith(')')) {
    expr = expr.slice(2, -1);
  } else {
    // Envolvemos en negativo: -(expresión)
    expr = `-( ${expr} )`;
  }
  updateDisplay();
}

/** Divide la expresión entre 100 (convierte a porcentaje). Ej: 25 → 25/100 = 0.25 */
function percent() {
  if (!expr) return;
  expr = `(${expr})/100`;
  updateDisplay();
}


// ── MODO DEG / RAD ───────────────────────────────────────────────

/**
 * Alterna entre modo Grados (DEG) y Radianes (RAD) para las funciones trigonométricas.
 * En modo DEG: sin(90) = 1   |   En modo RAD: sin(π/2) = 1
 */
function toggleMode() {
  isDeg = !isDeg;  // Invertir el valor booleano
  // Actualizar los indicadores DEG/RAD de la pantalla LCD
  document.getElementById('ind-deg').style.opacity = isDeg ? '1'    : '0.25';
  document.getElementById('ind-rad').style.opacity = isDeg ? '0.25' : '1';
}


// ── CALCULAR (presionar =) ───────────────────────────────────────

/**
 * Función principal: toma la expresión construida, la convierte al
 * formato que entiende Python y la envía al backend por HTTP.
 * Es async porque fetch() es una operación asíncrona (espera la respuesta).
 */
async function pressEquals() {
  if (!expr.trim()) return;  // No hacer nada si la expresión está vacía

  // Paso 1: convertir símbolos visuales a operadores de Python
  // Ejemplo: "3×4÷2" → "3*4/2"
  let apiExpr = expr;
  for (const [sym, rep] of Object.entries(DISPLAY_TO_API)) {
    apiExpr = apiExpr.split(sym).join(rep);
  }

  // Paso 2: si estamos en modo grados, avisar al backend
  // El backend convierte sind(30) → sin(math.radians(30))
  if (isDeg) {
    apiExpr = apiExpr.replace(/\b(sin|cos|tan)\(/g, '$1d(');
  }

  try {
    // Paso 3: enviar la expresión al backend con fetch()
    // fetch() hace una petición HTTP POST a nuestra API
    const res = await fetch('/api/calcular/expresion', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },  // Indicamos que enviamos JSON
      body: JSON.stringify({ expresion: apiExpr }),       // Convertimos el objeto a texto JSON
    });

    // Paso 4: leer la respuesta del servidor (también en JSON)
    const data = await res.json();

    // Si el servidor respondió con error (código 400 o similar), mostrar el mensaje
    if (!res.ok) {
      showError(data.detail || 'Error');
      return;
    }

    // Paso 5: mostrar el resultado en pantalla
    ans    = data.resultado;   // Guardar en ANS para reutilizar
    result = data.resultado;   // Guardar como último resultado
    document.getElementById('expression-display').textContent = expr + ' =';  // Mostrar "expr ="
    document.getElementById('main-display').textContent = result;
    document.getElementById('error-display').textContent = '';
    expr = result;    // La expresión pasa a ser el resultado (para encadenar)
    justCalc = true;  // Marcar que acabamos de calcular
    document.getElementById('preview-display').textContent = '';  // Limpiar preview

  } catch {
    // Este error ocurre si el servidor no responde (por ejemplo, si está apagado)
    showError('Sin conexión con el servidor');
  }
}


// ── MEMORIA ──────────────────────────────────────────────────────

/** M+: suma el resultado actual al valor guardado en memoria. */
function memoryAdd() {
  memory += parseFloat(result) || 0;
}

/** M-: resta el resultado actual al valor guardado en memoria. */
function memorySubtract() {
  memory -= parseFloat(result) || 0;
}

/** MR (Memory Recall): inserta el valor de memoria en la expresión actual. */
function memoryRecall() {
  justCalc = false;
  expr += String(memory);
  updateDisplay();
}

/** MC (Memory Clear): borra el valor guardado en memoria (lo pone en 0). */
function memoryClear() {
  memory = 0;
}


// ── TECLADO FÍSICO ───────────────────────────────────────────────
// Permite usar la calculadora con el teclado del computador.
// El evento 'keydown' se dispara cada vez que el usuario presiona una tecla.
document.addEventListener('keydown', (e) => {
  const k = e.key;
  if (k >= '0' && k <= '9') { insertTxt(k); return; }              // Dígitos 0-9
  if (k === '+') { insertTxt('+'); return; }                        // Suma
  if (k === '-') { insertTxt('−'); return; }                        // Resta
  if (k === '*') { insertTxt('×'); return; }                        // Multiplicación
  if (k === '/') { e.preventDefault(); insertTxt('÷'); return; }   // División (prevenir búsqueda del browser)
  if (k === '^') { insertTxt('^'); return; }                        // Potencia
  if (k === '(') { insertTxt('('); return; }                        // Paréntesis abre
  if (k === ')') { insertTxt(')'); return; }                        // Paréntesis cierra
  if (k === '.') { insertTxt('.'); return; }                        // Decimal
  if (k === 'Enter' || k === '=') { pressEquals(); return; }        // Calcular
  if (k === 'Backspace') { backspace(); return; }                    // Borrar
  if (k === 'Escape') { allClear(); return; }                        // Limpiar todo
  if (k === 'Delete') { clearEntry(); return; }                      // Limpiar entrada
});


// ── INICIALIZACIÓN ───────────────────────────────────────────────
// Esta línea se ejecuta cuando el navegador carga la página por primera vez.
// Inicializa el display mostrando "0".
updateDisplay('0');

