use std::{
    hint::black_box,
    time::{Duration, Instant},
};

use rand::{rng, seq::SliceRandom, Rng};
use rdst::RadixSort;
use static_search_tree::{eytzinger::Eytzinger, s_tree::STree16, SearchIndex};

type T = u32;

/// Generate a sorted list of n random integers.
fn random_perm(n: usize) -> Vec<T> {
    let mut v: Vec<T> = (0..n as T).collect();
    v.shuffle(&mut rng());
    v
}

fn time<T>(f: impl FnOnce() -> T) -> Duration {
    let start = Instant::now();
    black_box(f());
    start.elapsed()
}

fn inverse(v: &Vec<T>) -> Duration {
    let mut w = vec![0; v.len()];

    time(|| {
        for i in 0..v.len() {
            w[v[i] as usize] = i;
        }
        w
    })
}

fn inverse_sqrt(v: &Vec<T>) -> Duration {
    let n = v.len();
    let mut w = vec![0; n];
    let bits = n.ilog2() / 2;

    let max = (n >> bits) + 1;

    let mut buf = vec![(0, 0); n];
    let mut bufpos = vec![0; max];
    for (i, bp) in bufpos.iter_mut().enumerate() {
        *bp = i << bits;
    }

    time(|| {
        for i in 0..n {
            let b = v[i] as usize >> bits;
            let bp = bufpos[b];
            bufpos[b] += 1;
            buf[bp] = (v[i], i as u32);
        }
        for (x, i) in buf {
            w[i as usize] = x;
        }
        w
    })
}

fn inverse_sort(v: &Vec<T>) -> Duration {
    let n = v.len();

    let mut buf = vec![0; n];
    for i in 0..n {
        buf[i] = ((v[i] as u64) << 32) + i as u64;
    }

    time(|| {
        buf.radix_sort_builder()
            .with_parallel(false)
            .with_single_threaded_tuner()
            .sort();
        // buf.radix_sort_unstable();
        buf
    })
}

fn square(v: &Vec<T>) -> Duration {
    let mut w = vec![0; v.len()];

    time(|| {
        for i in 0..v.len() {
            w[i] = v[v[i] as usize];
        }
        w
    })
}

fn test(n: usize) -> Vec<Duration> {
    let v = &random_perm(n);

    vec![
        inverse(v),
        // inverse_sqrt(v),
        // inverse_sort(v),
        square(v),
    ]
}

fn main() {
    let mut ns = vec![];
    for i in 0.. {
        let n = ((1234. * 1.3f32.powi(i)) as usize).next_multiple_of(2);
        if n > 10000000000 {
            break;
        }
        ns.push(n);
    }

    for &n in &ns {
        let out = test(n);
        eprint!("n {n:>10}");
        for mut x in out {
            let y = x.as_secs_f32() * (1000f32).powf(3.) / n as f32;
            eprint!(" {y:>4.1}");
        }
        eprintln!();
    }
}
