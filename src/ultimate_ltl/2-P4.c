//#Safe
//@ ltl invariant positive: [] (AP(a == 1) ==> <> AP(r == 1));

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
    __VERIFIER_assume(n > 100);
    while(1)
    {

        int choice = __VERIFIER_nondet_int();
        if (choice > 0) {
            a = 1;
            if (choice > 1) {
                n = n - 1;
            } else {
                n = n;
            }
            if (n <= 0) {
                r = 1;
            } else {
                r = 0;
            }
        } else {
            // stay
        }
    }
}
