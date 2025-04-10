
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
            if (nondet % 2 == 0) {
                // move robot 1
                x_1 = x_1 + 1 + (nondet % 3);
            }  else {
                y_2 = y_2 + 1 + (nondet % 3);
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
