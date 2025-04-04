//#Safe
//@ ltl invariant positive: [] <> AP(x <= 0);

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int x, y;

int main()
{
    x = __VERIFIER_nondet_int();
    y = __VERIFIER_nondet_int();
    while(1)
    {
        if (x > 0) {
            int a = __VERIFIER_nondet_int();
            if (a > 0 && x >= y) {
                x = x + 1;
            } else {
                x = x - 1;
            }
        }
        else {
            x = x;
        }
    }
}
