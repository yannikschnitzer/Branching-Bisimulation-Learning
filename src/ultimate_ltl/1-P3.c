//#Safe
//@ ltl invariant positive: [] <> AP(n > 0);

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int a, r, n;

int main()
{
    a = __VERIFIER_nondet_int();
    r = 0;
    n = __VERIFIER_nondet_int();
    __VERIFIER_assume(n >= 15);
    while(1)
    {

        int choice = __VERIFIER_nondet_int();
        if (choice > 0) {
            if (a == 1) {
                a = 0;
            } else {
                a = 1;
            }
            if (r == 1) {
                r = 1;
            } else {
                r = 0;
            }
            n = n;
        } else {
            // stay
        }
    }
}
