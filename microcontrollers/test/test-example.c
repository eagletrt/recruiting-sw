/*!
 * \file test-example.c
 * \date 2026-30-9
 * \author Alessandro Giustina [giustinalessandro@gmail.com]
 *
 * \brief Example test file
 */

#include "unity.h"
#include "example-api.h"
// Include the FFF library for function mocking (must be pasted into test/include/fff.h)
#include "fff.h"

void setUp(void) {
    // Here any initialization code can be placed that needs to run before each test
}

void tearDown(void) {
    // Here any cleanup code can be placed that needs to run after each test
}

void testSomething(void) {
    // Example test case
    int result = exampleFunction(5);
    TEST_ASSERT_EQUAL(10, result); // Assuming exampleFunction doubles the input
}

void testAnotherThing(void) {
    // Another example test case
    int result = anotherExampleFunction(3);
    TEST_ASSERT_EQUAL(9, result); // Assuming anotherExampleFunction squares the input
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(testSomething);
    RUN_TEST(testAnotherThing);
    return UNITY_END();
}