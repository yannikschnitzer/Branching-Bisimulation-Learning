//#Safe
//@ ltl invariant positive: [] <> AP(w != 1);

#include <stdio.h> 

extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern void __VERIFIER_assume() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_int() __attribute__ ((__noreturn__));

int w, g;

int main()
{
    w = __VERIFIER_nondet_int();
    g = __VERIFIER_nondet_int();
    while(1)
    {
        int choice = __VERIFIER_nondet_int();
        if (choice > 0) {
            w = 0;
            if (g >= 0) {
                g = 0;
            } else {
                g = g;
            }
        } else {
            w = 1;
            if (g >= 0) {
                g = 0;
            } else {
                g = g;
            }
        }
    }
}
