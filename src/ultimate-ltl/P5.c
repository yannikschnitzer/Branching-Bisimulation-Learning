//#Safe
//@ ltl invariant positive: AP(p < i) ==> <> [] AP(u = 1);

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int i, p, s, u;

int main()
{
    i = __VERIFIER_nondet_int();
    p = __VERIFIER_nondet_int();
    s = __VERIFIER_nondet_int();
    u = __VERIFIER_nondet_int();
    while(1)
    {

        int choice = __VERIFIER_nondet_int();
        if (choice > 0) {
            if (i < p) {
                i = i;
                u = 1;
            } else {
                i = i + 1;
                u = u;
            }
            s = 1;
        } else {
            s = 1;
            u = 1;
        }
    }
}
