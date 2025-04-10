
#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int x_1, y_2, clash;

int main()
{
    x_1 = __VERIFIER_nondet_int();
    y_2 = __VERIFIER_nondet_int();
    while(1)
    {
        clash = x_1 == 0 && y_2 == 0;
        if (clash) {
            x_1 = x_1;
            y_2 = y_2;
        } else {
            int nondet = __VERIFIER_nondet_int();
            int robot_to_move = nondet % 2;
            int action = nondet % 3;
            if (robot_to_move == 0) {
                if (x_1 <= 0 || action == 0) {
                    x_1 = x_1 + 1;
                } else if (action == 1) {
                    x_1 = x_1 * 2;
                } else {
                    x_1 = x_1 * x_1;
                }
            } else {
                if (y_2 <= 0 || action == 0) {
                    y_2 = y_2 + 1;
                } else if (action == 1) {
                    y_2 = y_2 * 2;
                } else {
                    y_2 = y_2 * y_2;
                }
            }
        }
        /*
        else if (x >= 1) {
            int a = __VERIFIER_nondet_int();
            if (a > 0) {
                x = x - 1;
            } else {
                x = x + 1;
            }
        }
        */
    }
}
