from __future__ import print_function
import tensorflow as tf
import numpy as np
import pytest
import sys
from tensorflow.python.ops import array_ops

rows = 10
cols = 15


def test_indexing():
    with tf.Graph().as_default():
        with tf.device('/gpu:0'):
            tf_a = tf.placeholder(tf.float32, [rows, cols], 'a')
            tf_out = tf_a[0]
            tf_out2 = tf_a[0:3]
            tf_out3 = tf.transpose(tf_a)[0:3]

            a = np.random.randn(rows, cols).astype(np.float32)
            with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
                out, out2, out3 = sess.run((tf_out, tf_out2, tf_out3), {tf_a: a})
            # print('a', a)
            print('out', out)
            print('a[0]', a[0])
            assert np.all(a[0] == out)

            print('a[0:3]', a[0:3])
            print('out2', out2)
            assert np.all(a[0:3] == out2)

            print('a.T[0:3]', a.T[0:3])
            print('out3', out3)
            assert np.all(a.T[0:3] == out3)


def test_slice():
    with tf.Graph().as_default():
        with tf.device('/gpu:0'):
            # tf_a = tf.placeholder(tf.float32, [rows, cols], 'a')
            tf_a = tf.Variable(np.random.randn(rows, cols).astype(np.float32))
            tf_out = tf.slice(tf_a, [1, 2], [2, 1])
            tf_out2 = array_ops.slice(tf_a, [1, 2], [2, 1])

            a = np.random.randn(rows, cols).astype(np.float32)
            with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
                sess.run(tf.initialize_all_variables())
                out, out2 = sess.run((tf_out, tf_out2))
            print('a', a)
            print('out', out)
            print('out2', out2)
            # diff = np.abs(gpu_out - expected).max()
            # print('diff', diff)
            # assert diff <= 1e-4


def test_strided_slice():
    with tf.Graph().as_default():
        with tf.device('/gpu:0'):
            tf_a = tf.placeholder(tf.float32, [rows, cols], 'a')
            tf_out = tf.strided_slice(tf_a, [1, 0], [2, 0], [2, 1])

            a = np.random.randn(rows, cols).astype(np.float32)
            with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
                out = sess.run(tf_out, {tf_a: a})
            print('a', a)
            print('out', out)
            # diff = np.abs(gpu_out - expected).max()
            # print('diff', diff)
            # assert diff <= 1e-4


def test_concat():
    with tf.Graph().as_default():
        with tf.device('/gpu:0'):
            tf_a = tf.placeholder(tf.float32, [rows, cols], 'a')
            tf_b = tf.placeholder(tf.float32, [rows, cols], 'a')
            tf_out = tf.concat(0, [tf_a, tf_b])
            tf_out1 = tf.concat(1, [tf_a, tf_b])

            a = np.random.randn(rows, cols).astype(np.float32)
            b = np.random.randn(rows, cols).astype(np.float32)
            with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
                out, out1 = sess.run((tf_out, tf_out1), {tf_a: a, tf_b: b})
            print('a', a)
            print('out', out)
            print('out1', out1)
            # diff = np.abs(gpu_out - expected).max()
            # print('diff', diff)
            # assert diff <= 1e-4


def test_concat2():
    graph = tf.Graph()
    with graph.as_default():
        with tf.device('/gpu:0'):
            a_tf = tf.placeholder(tf.float32, [None, None])
            b_tf = tf.placeholder(tf.float32, [None, None])
            a = np.random.randn(3, 2).astype(np.float32)
            b = np.random.randn(3, 2).astype(np.float32)
            a2_tf = a_tf * 2
            b2_tf = b_tf + 2
            print()
            # print('a', a)
            # print('b', b)
            c_tf = tf.concat(values=[a2_tf, b2_tf], concat_dim=1)
            sess = tf.Session()
            with sess.as_default():
                # print(sess.run(a_tf, feed_dict={a_tf: np.random.randn(3).astype(np.float32)}))
                a2, b2, c = sess.run((a2_tf, b2_tf, c_tf), feed_dict={a_tf: a, b_tf: b})
                print(a2)
                print(b2)
                print(c)


@pytest.mark.parametrize(
    'shape',
    [
        (3, 4),
        (50, 70, 12),
        (20, 128, 64)
    ])
def test_pack(shape):
    graph = tf.Graph()
    with graph.as_default():
        with tf.device('/gpu:0'):
            a_tf = tf.placeholder(tf.float32, shape)
            # b_tf = tf.placeholder(tf.float32, [None, None])
            a = np.random.randn(*shape).astype(np.float32)
            # b = np.random.randn(3, 2).astype(np.float32)
            # a2_tf = a_tf * 2
            # b2_tf = b_tf + 2
            # print()
            # print('a', a)
            # print('b', b)
            c_tf = tf.pack(values=[a_tf])
            sess = tf.Session()
            with sess.as_default():
                # print(sess.run(a_tf, feed_dict={a_tf: np.random.randn(3).astype(np.float32)}))
                c = sess.run(c_tf, feed_dict={a_tf: a})
                print('a.shape', a.shape)
                print('c.shape', c.shape)
                if(np.prod(a.shape)) < 20:
                    print('a', a)
                    print('c', c)
                assert c.shape[0] == 1
                assert c.shape[1:] == a.shape
                assert np.all(c[0] == a)
                # print(b2)
                # print(c)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please run using py.test')
    else:
        eval('%s()' % sys.argv[1])
