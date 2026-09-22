# Embedded Coding Styles

> The keywords **MUST**, **MUST NOT**, **REQUIRED,** **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14) [[RFC2119](https://www.rfc-editor.org/rfc/rfc2119)] [[RFC8174](https://www.rfc-editor.org/rfc/rfc8174)]


This document provides an overview of the **coding styles** which have to be followed while developing code for **any** embedded firmware, the following statements MUST always be taken into consideration:

* Rules MAY be proposed in the *To be approved* section and must be approved by the majority of the people belonging to the **Embedded Workgroup** to be officially adopted
* The **total number of approved rules** is not limited but SHOULD be kept **as low as possible** to allow everyone to remember them easily, since having too many rules may be counterproductive
* It is RECOMMENDED to use as many **tools** as possible to automatically check and/or enforce the approved rules so that they are always respected
* Any rule can be added, edited or removed at any time if the decision is made by the majority of the **Embedded Workgroup**
* Rules MAY be grouped into different categories and they MUST have a **unique code** (e.g. Rule-G0), **definition** (inside the /Tip notice) and **rationale** to explain why the rule is needed. **Examples** MAY be added for further clarification



---


# Approved Rules

## General rules

### Rule-G0



**English MUST be used inside the codebase, no other language is allowed**


**RATIONALE**: Since English is one of the most popular languages across the world and it is accepted as the **common language** that should be used to communicate between people of different countries, the code is needed to be written in English to be understood by everyone.

**EXAMPLES**:

```clike
/* OK */
// This is a comment

int function(int argument) {
    return argument;
}

/* Wrong */
// Questo è un commento

int funzione(int argomento) {
    return argomento;
}
```

### Rule-G1



`**clang-format**` **MUST always be used as formatter with the provided** `**.clang-format**` **configuration file**


**RATIONALE:** The usage of a code formatter helps to keep the code style **consistent** if multiple people are working on it, improving maintainability of the codebase. It also helps by keeping a cleaner git history with only the important changes.

Clang Format is one of the most known and widely used code formatter tool, it was chosen for its ease of use, customizability and support.

### Rule-G2


`extern` **MUST NOT** **be used unless strictly necessary**

**RATIONALE**: The `extern` keyword is implicit for non static functions, but for variables it can be used to share the same global variable across different files. This may increase code complexity as well as make code difficult to read and maintain. Having multiple variables with the same name and an `extern` definition may cause unwanted behavior.

### Rule-G3

**Pointers MUST be compared against** `NULL` **instead of using boolean operators**

**RATIONALE**: When comparing pointers against `NULL` it may be misleading as well as difficult to read and maintain to use them as boolean operators. Since a pointer is basically an integer value boolean operators apply to it following the C integer to boolean logic which is: `0 = false` and `non zero = true`. Comparison against `NULL` is universal and has no ambiguity therefore it is recommended to use it.

**EXAMPLES:**

```clike
/* OK */
void foo(int *p) {
    if (p == NULL)
        return;
}

/* Wrong */
void foo(int *p) {
    if (!p)
        return;
}
```

## Comments

### Rule-C0


**Doxygen Qt style comments MUST be used to document functions, structures, enums, etc...**

**RATIONALE**: Code documentation is needed to make other programmers fully understand the logic behind the program implementation, doxygen helps by giving a standard and clean way of writing in-code documentation as well as provide tools for automatic documentation generation. The Qt style was chosen just to keep the comment style consistent across all platforms.

**EXAMPLES**:

```clike
/*!
 * \brief Get the n-th fibonacci sequence number.
 *
 * Given the index of the series returnes the fibonacci number in the sequence
 * at that index.
 *
 * \details The sequence starts at index 0 with the value of 0 and the next
 * value is one.
 *
 * \attention Negative index numbers are not valid indices.
 *
 * \param n The index of the fibonacci number.
 * \return The n-th fibonacci number.
 */
int fibonacci(int n);
```

## Naming

### **Rule-N0**

**Identifiers naming MUST follow the requirements defined in table 1 and MUST be checked with tools such as** `**clang-tidy**` **whenever possible**


*Table 1:*

| **IDENTIFIER** | **CASE** | **REQUIREMENTS** | **RATIONALE** |
|------------|:----:|--------------|-----------|
| **ANY**    |      | * Any number of underscores `_` MUST NOT be used as prefix | * Underscore `_` prefixes are reserved for the C language itself and SHOULD NOT be used in user code since it may cause naming conflicts with other identifiers |
| **Variables** | `snake_case` | * The name of the file MUST be used as prefix for global variables (e.g. `module_name_<variable name>`) | * Prefixing variables is often used to reduce the probability of naming conflicts |
| **Functions** | `snake_case` | * `prv_` MUST be used as prefix for module-private (*static*) functions <br> * `int_` MUST be used as prefix for library internal functions which SHOULD NOT be used by user application but has to be used across different files | * Prefixing functions is useful as documentation and to show the intent of the developer to users of the program or library |
| **Structs** | `PascalCase` | * Structures MUST NOT be redefined using `typedef` | * As described inside the [Linux Kernel Coding Standard](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#naming) using `typedef` on structures obscures the variable type |
| **Unions** | `PascalCase` | * Unions MUST NOT be redefined using `typedef` | * As described inside the [Linux Kernel Coding Standard](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#naming) using `typedef` on unions obscures the variable type |
| **Enums/Members** | `PascalCase/SCREAMING_SNAKE_CASE` | * Enums MUST NOT be redefined using `typedef` <br> * Members of the enum MUST be prefixed with the enum name in `SCREAMING_SNAKE_CASE` | * As described inside the [Linux Kernel Coding Standard](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#naming) using `typedef` on enums obscures the variable type <br> * Prefixing the enum members reduces the probability of naming conflicts with other enums or macros |
| **Macros** | `SCREAMING_SNAKE_CASE` | * Parentheses MUST be put around the whole macro (e.g. `#define FOO(expr) (expr)`) <br> * Parentheses MUST be put around macro parameters (e.g. `#define MIN(a, b) ((a) < (b) ? (a) : (b))`) <br> * Multiline macros MUST be enclosed with a `do { } while(0)` (e.g. `#define FOO() do { \ <multiline expression> \ } while(0)` | * Since macros are evaluated by the preprocessor to avoid conflicts with external identifiers it is a good practice to wrap the macro with parentheses <br> * Since a macro parameter can also be an expression to avoid unpredictable behavior caused by operator precedence it is a good practice to wrap parameters with parentheses (e.g. `#define MUL(a, b) (a * b)`: writing `MUL(2, 3 + 5)` evaluates to `2 * 3 + 5 = 11` instead of `2 * (3 + 5) = 16`) <br> * Multiline macros are prone to errors (e.g. using the macro in a single line conditional expression `if(<condition>) <MULTILINE MACRO>;`, to avoid any possible problem the macro can be wrapped into a `do { } while(0)` to group all lines into a single expression and allowing the user to put the semicolon `;` at the end of the statement without errors |
| **Typedefs** | `snake_case` | * `_t` MUST NOT be used as suffix | * `_t` prefix is reserved for the C language type redefinitions and SHOULD NOT be used in user code since it may cause naming conflicts with other identifiers |
| **Filenames** | `kebab-case` |              |           |
| **Booleans** | `snake_case` | * Booleans should be defined using the `<stdbool.h>` header | * The use of bool (introduced in **C99**) is explicit, type-safe, and self-documenting <br> * While some legacy or safety-critical guidelines discourage bool for backward-compatibility reasons, modern C standards and toolchains explicitly allow _Bool and `<stdbool.h>` |



---