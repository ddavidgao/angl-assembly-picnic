.text
.globl _optimize_picnic_kernel
.p2align 2

// int32_t optimize_picnic_kernel(PicnicRequest *req)
//
// PicnicRequest layout:
//   int32_t count          offset 0
//   int32_t max_weight     offset 4
//   int32_t heat           offset 8
//   int32_t rain           offset 12
//   int32_t *weights       offset 16
//   int32_t *happiness     offset 24
//   int32_t *heat_penalty  offset 32
//   int32_t *rain_penalty  offset 40
//   uint32_t out_mask      offset 48
//   int32_t out_weight     offset 52
//
// This is the generated implementation for the Angl chapter. It enumerates
// every subset mask, scores it, and writes the best mask/weight back to req.

_optimize_picnic_kernel:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    stp x19, x20, [sp, #-16]!
    stp x21, x22, [sp, #-16]!
    stp x23, x24, [sp, #-16]!
    stp x25, x26, [sp, #-16]!
    stp x27, x28, [sp, #-16]!

    mov x19, x0              // req
    ldr w20, [x19, #0]       // count
    ldr w21, [x19, #4]       // max_weight
    ldr w22, [x19, #8]       // heat
    ldr w23, [x19, #12]      // rain
    ldr x24, [x19, #16]      // weights
    ldr x25, [x19, #24]      // happiness
    ldr x26, [x19, #32]      // heat_penalty
    ldr x27, [x19, #40]      // rain_penalty

    mov w28, #1
    lsl w28, w28, w20        // limit = 1 << count
    mov w8, #0               // mask
    mov w9, #0               // best_score
    mov w10, #0              // best_mask
    mov w11, #0              // best_weight

mask_loop:
    cmp w8, w28
    b.ge done_masks

    mov w12, #0              // i
    mov w13, #0              // total_weight
    mov w14, #0              // score

item_loop:
    cmp w12, w20
    b.ge score_mask

    mov w15, #1
    lsl w15, w15, w12
    tst w8, w15
    b.eq next_item

    uxtw x16, w12
    ldr w17, [x24, x16, lsl #2]
    add w13, w13, w17

    ldr w17, [x25, x16, lsl #2]
    add w14, w14, w17

    cmp w22, #7
    b.lt skip_heat
    ldr w17, [x26, x16, lsl #2]
    sub w14, w14, w17

skip_heat:
    cmp w23, #6
    b.lt next_item
    ldr w17, [x27, x16, lsl #2]
    sub w14, w14, w17

next_item:
    add w12, w12, #1
    b item_loop

score_mask:
    cmp w13, w21
    b.gt next_mask
    cmp w14, w9
    b.le next_mask
    mov w9, w14
    mov w10, w8
    mov w11, w13

next_mask:
    add w8, w8, #1
    b mask_loop

done_masks:
    str w10, [x19, #48]
    str w11, [x19, #52]
    mov w0, w9

    ldp x27, x28, [sp], #16
    ldp x25, x26, [sp], #16
    ldp x23, x24, [sp], #16
    ldp x21, x22, [sp], #16
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret
