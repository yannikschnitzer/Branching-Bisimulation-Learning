
//#Safe
//@ ltl invariant positive: <>([] AP(x >= -1) && [] AP(x <= 1));

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int x;

int main()
{
    x = __VERIFIER_nondet_int();
    while(1)
    {
        if (x < -1) {
            x = x - 1;
        } else if (x > 1) {
            int a = __VERIFIER_nondet_int();
            if (a > 0) {
                x = x - 1;
            } else {
                x = x + 1;
            }
        }
        else {
            x = x;
        }
    }
}
