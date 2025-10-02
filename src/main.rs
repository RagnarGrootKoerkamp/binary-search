use std::{
    hint::black_box,
    time::{Duration, Instant},
};

use rand::{rng, Rng};
use rdst::RadixSort;
use static_search_tree::{eytzinger::Eytzinger, s_tree::STree16, SearchIndex};

type T = u32;

/// Generate a sorted list of n random integers.
fn random_sorted_vec(n: usize) -> Vec<T> {
    let mut rng = rng();
    let mut v: Vec<T> = (0..n).map(|_| rng.random_range(0..i32::MAX as T)).collect();
    v.radix_sort_unstable();
    v
}

fn random_vec(n: usize) -> Vec<T> {
    let mut rng = rng();
    (0..n).map(|_| rng.random_range(0..i32::MAX as T)).collect()
}

fn binary_search(v: &[T], x: T) -> usize {
    let mut l = 0;
    // inclusive right end
    let mut h = v.len() - 1;
    while l < h {
        let m = (l + h + 1) / 2;
        if x < v[m] {
            h = m - 1;
        } else {
            l = m;
        }
    }
    l
}

fn sqrt_search(v: &[T], x: T, stride: usize, block: &[T]) -> usize {
    let mut cnt = 0;
    for &v in block {
        cnt += (x >= v) as usize;
    }
    // eprintln!("cnt {cnt:?}");
    let offset = cnt * stride;
    let mut pos = 0;
    for &v in &v[offset.min(v.len())..(offset + stride).min(v.len())] {
        pos += (x >= v) as usize;
    }
    // eprintln!("pos {pos:?}");
    offset + pos
}

fn test(n: usize, q: usize) -> [Duration; 5] {
    let data = random_sorted_vec(n);
    let lookup = {
        let mut rng = rng();
        let queries = (0..q)
            .map(|_| rng.random::<T>() as usize % n)
            .collect::<Vec<_>>();

        let start = Instant::now();

        let mut seed = 0;
        for &q in &queries {
            seed = data[q ^ seed] as usize & 1;
        }

        start.elapsed()
    };

    let bs = {
        let queries = random_vec(q);

        let start = Instant::now();

        let mut seed = 0;
        for &q in &queries {
            seed = binary_search(&data, q ^ seed) as T & 1;
        }
        black_box(seed);

        start.elapsed()
    };

    // let sqrt = {
    //     let data = random_sorted_vec(n);
    //     let queries = random_vec(q);
    //     let stride = n.isqrt();
    //     let block: Vec<T> = (0..n).step_by(stride).map(|i| data[i]).collect();
    //     // eprintln!("{stride:?} {block:?}");

    //     let start = Instant::now();

    //     let mut seed = 0;
    //     for &q in &queries {
    //         seed = sqrt_search(&data, q ^ seed, stride, &block) as T & 1;
    //     }
    //     black_box(seed);

    //     start.elapsed()
    // };
    let sqrt = Duration::default();

    let e = {
        let et = Eytzinger::new(&data);

        let queries = random_vec(q);

        let start = Instant::now();

        let mut seed = 0;
        for &q in &queries {
            seed = et.search_prefetch::<4>(q ^ seed);
        }
        black_box(seed);

        start.elapsed()
    };

    let s = {
        // let data = random_sorted_vec(n);
        // let st = STree16::new(&data);

        // let queries = random_vec(q);

        let start = Instant::now();

        // let mut seed = 0;
        // for &q in &queries {
        //     seed = st.search(q ^ seed);
        // }
        // black_box(seed);

        start.elapsed()
    };

    [lookup, bs, sqrt, e, s]
}

fn main() {
    let mut ns = vec![];
    for i in 0.. {
        let n = ((1234. * 1.2f32.powi(i)) as usize).next_multiple_of(2);
        if n > 4 * 10usize.pow(9) / 4 {
            break;
        }
        ns.push(n);
    }

    let q = 1000000;

    for &n in &ns {
        let out = test(n, q);
        print!("{n}");
        eprint!("n {n:>10}");
        for x in out {
            let y = x.as_secs_f32() * (1000f32).powf(3.) / q as f32;
            print!(",{y:>6.3}");
            eprint!(" {y:>4.1}");
        }
        println!();
        eprintln!();
    }
}
