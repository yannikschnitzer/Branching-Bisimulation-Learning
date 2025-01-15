//#Safe
//@ ltl invariant positive: AP(r < a) ==> <> [] AP(r < a);
// ltl invariant positive: [] <> AP(n > 0);
// ltl invariant positive: [] AP(n >= 0);
// ltl invariant positive: <> AP(a == 1);

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
            if (n > 0) {
                a = 1;
                r = r;
                n = n - 1;
            } else {
                a = 1;
                r = 1;
                n = n;
            }
        } else {
            // stay
        }
    }
}
