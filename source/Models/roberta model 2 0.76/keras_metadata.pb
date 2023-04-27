
�;root"_tf_keras_network*�:{"name": "model_16", "trainable": true, "expects_training_arg": true, "dtype": "float32", "batch_input_shape": null, "must_restore_from_config": false, "preserve_input_structure_in_config": false, "autocast": false, "class_name": "Functional", "config": {"name": "model_16", "trainable": true, "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "input_49"}, "name": "input_49", "inbound_nodes": []}, {"class_name": "InputLayer", "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "input_50"}, "name": "input_50", "inbound_nodes": []}, {"class_name": "Reshape", "config": {"name": "reshape_32", "trainable": true, "dtype": "float32", "target_shape": {"class_name": "__tuple__", "items": [1024, 1]}}, "name": "reshape_32", "inbound_nodes": [[["input_49", 0, 0, {}]]]}, {"class_name": "Reshape", "config": {"name": "reshape_33", "trainable": true, "dtype": "float32", "target_shape": {"class_name": "__tuple__", "items": [1024, 1]}}, "name": "reshape_33", "inbound_nodes": [[["input_50", 0, 0, {}]]]}, {"class_name": "Lambda", "config": {"name": "lambda_21", "trainable": true, "dtype": "float32", "function": {"class_name": "__tuple__", "items": ["4wEAAAAAAAAAAAAAAAcAAAAGAAAAQwAAAHNoAAAAfABkARkAfABkAhkAAgB9AX0CdABqAXwBfAIU\nAGQDZASNAn0DdACgAnQAagF0AKADfAGhAWQDZASNAqEBfQR0AKACdABqAXQAoAN8AqEBZANkBI0C\noQF9BXwDfAR8BRQAGwB9BnwGUwApBU7pAAAAAOkBAAAA6f////8pAdoEYXhpcykE2gFL2gNzdW3a\nBHNxcnTaBnNxdWFyZSkH2gF42gJ4MdoCeDLaC2RvdF9wcm9kdWN02gdub3JtX3gx2gdub3JtX3gy\n2hFjb3NpbmVfc2ltaWxhcml0eakAchAAAAD6IDxpcHl0aG9uLWlucHV0LTEwNC1hMmViZDUxMjI0\nZjQ+cg8AAAAEAAAAcwwAAAAAARIBEgEaARoBDAE=\n", null, null]}, "function_type": "lambda", "module": "__main__", "output_shape": null, "output_shape_type": "raw", "output_shape_module": null, "arguments": {}}, "name": "lambda_21", "inbound_nodes": [[["reshape_32", 0, 0, {}], ["reshape_33", 0, 0, {}]]]}, {"class_name": "Dense", "config": {"name": "dense_39", "trainable": true, "dtype": "float32", "units": 1, "activation": "sigmoid", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "name": "dense_39", "inbound_nodes": [[["lambda_21", 0, 0, {}]]]}], "input_layers": [["input_49", 0, 0], ["input_50", 0, 0]], "output_layers": [["dense_39", 0, 0]]}, "shared_object_id": 8, "input_spec": [{"class_name": "InputSpec", "config": {"dtype": null, "shape": {"class_name": "__tuple__", "items": [null, 1024]}, "ndim": 2, "max_ndim": null, "min_ndim": null, "axes": {}}}, {"class_name": "InputSpec", "config": {"dtype": null, "shape": {"class_name": "__tuple__", "items": [null, 1024]}, "ndim": 2, "max_ndim": null, "min_ndim": null, "axes": {}}}], "build_input_shape": [{"class_name": "TensorShape", "items": [null, 1024]}, {"class_name": "TensorShape", "items": [null, 1024]}], "is_graph_network": true, "full_save_spec": {"class_name": "__tuple__", "items": [[[{"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null, 1024]}, "float32", "input_49"]}, {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null, 1024]}, "float32", "input_50"]}]], {}]}, "save_spec": [{"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null, 1024]}, "float32", "input_49"]}, {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null, 1024]}, "float32", "input_50"]}], "keras_version": "2.12.0", "backend": "tensorflow", "model_config": {"class_name": "Functional", "config": {"name": "model_16", "trainable": true, "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "input_49"}, "name": "input_49", "inbound_nodes": [], "shared_object_id": 0}, {"class_name": "InputLayer", "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "input_50"}, "name": "input_50", "inbound_nodes": [], "shared_object_id": 1}, {"class_name": "Reshape", "config": {"name": "reshape_32", "trainable": true, "dtype": "float32", "target_shape": {"class_name": "__tuple__", "items": [1024, 1]}}, "name": "reshape_32", "inbound_nodes": [[["input_49", 0, 0, {}]]], "shared_object_id": 2}, {"class_name": "Reshape", "config": {"name": "reshape_33", "trainable": true, "dtype": "float32", "target_shape": {"class_name": "__tuple__", "items": [1024, 1]}}, "name": "reshape_33", "inbound_nodes": [[["input_50", 0, 0, {}]]], "shared_object_id": 3}, {"class_name": "Lambda", "config": {"name": "lambda_21", "trainable": true, "dtype": "float32", "function": {"class_name": "__tuple__", "items": ["4wEAAAAAAAAAAAAAAAcAAAAGAAAAQwAAAHNoAAAAfABkARkAfABkAhkAAgB9AX0CdABqAXwBfAIU\nAGQDZASNAn0DdACgAnQAagF0AKADfAGhAWQDZASNAqEBfQR0AKACdABqAXQAoAN8AqEBZANkBI0C\noQF9BXwDfAR8BRQAGwB9BnwGUwApBU7pAAAAAOkBAAAA6f////8pAdoEYXhpcykE2gFL2gNzdW3a\nBHNxcnTaBnNxdWFyZSkH2gF42gJ4MdoCeDLaC2RvdF9wcm9kdWN02gdub3JtX3gx2gdub3JtX3gy\n2hFjb3NpbmVfc2ltaWxhcml0eakAchAAAAD6IDxpcHl0aG9uLWlucHV0LTEwNC1hMmViZDUxMjI0\nZjQ+cg8AAAAEAAAAcwwAAAAAARIBEgEaARoBDAE=\n", null, null]}, "function_type": "lambda", "module": "__main__", "output_shape": null, "output_shape_type": "raw", "output_shape_module": null, "arguments": {}}, "name": "lambda_21", "inbound_nodes": [[["reshape_32", 0, 0, {}], ["reshape_33", 0, 0, {}]]], "shared_object_id": 4}, {"class_name": "Dense", "config": {"name": "dense_39", "trainable": true, "dtype": "float32", "units": 1, "activation": "sigmoid", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}, "shared_object_id": 5}, "bias_initializer": {"class_name": "Zeros", "config": {}, "shared_object_id": 6}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "name": "dense_39", "inbound_nodes": [[["lambda_21", 0, 0, {}]]], "shared_object_id": 7}], "input_layers": [["input_49", 0, 0], ["input_50", 0, 0]], "output_layers": [["dense_39", 0, 0]]}}, "training_config": {"loss": "binary_crossentropy", "metrics": [[{"class_name": "MeanMetricWrapper", "config": {"name": "pearson_correlation", "dtype": "float32", "fn": "pearson_correlation"}, "shared_object_id": 11}, {"class_name": "MeanMetricWrapper", "config": {"name": "mae", "dtype": "float32", "fn": "mean_absolute_error"}, "shared_object_id": 12}, {"class_name": "MeanMetricWrapper", "config": {"name": "mse", "dtype": "float32", "fn": "mean_squared_error"}, "shared_object_id": 13}]], "weighted_metrics": null, "loss_weights": null, "optimizer_config": {"class_name": "Custom>Adam", "config": {"name": "Adam", "weight_decay": null, "clipnorm": null, "global_clipnorm": null, "clipvalue": null, "use_ema": false, "ema_momentum": 0.99, "ema_overwrite_frequency": null, "jit_compile": true, "is_legacy_optimizer": false, "learning_rate": 0.0010000000474974513, "beta_1": 0.9, "beta_2": 0.999, "epsilon": 1e-07, "amsgrad": false}}}}2
�root.layer-0"_tf_keras_input_layer*�{"class_name": "InputLayer", "name": "input_49", "dtype": "float32", "sparse": false, "ragged": false, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "input_49"}}2
�root.layer-1"_tf_keras_input_layer*�{"class_name": "InputLayer", "name": "input_50", "dtype": "float32", "sparse": false, "ragged": false, "batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "config": {"batch_input_shape": {"class_name": "__tuple__", "items": [null, 1024]}, "dtype": "float32", "sparse": false, "ragged": false, "name": "input_50"}}2
�root.layer-2"_tf_keras_layer*�{"name": "reshape_32", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "preserve_input_structure_in_config": false, "autocast": true, "class_name": "Reshape", "config": {"name": "reshape_32", "trainable": true, "dtype": "float32", "target_shape": {"class_name": "__tuple__", "items": [1024, 1]}}, "inbound_nodes": [[["input_49", 0, 0, {}]]], "shared_object_id": 2, "build_input_shape": {"class_name": "TensorShape", "items": [null, 1024]}}2
�root.layer-3"_tf_keras_layer*�{"name": "reshape_33", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "preserve_input_structure_in_config": false, "autocast": true, "class_name": "Reshape", "config": {"name": "reshape_33", "trainable": true, "dtype": "float32", "target_shape": {"class_name": "__tuple__", "items": [1024, 1]}}, "inbound_nodes": [[["input_50", 0, 0, {}]]], "shared_object_id": 3, "build_input_shape": {"class_name": "TensorShape", "items": [null, 1024]}}2
�	root.layer-4"_tf_keras_layer*�	{"name": "lambda_21", "trainable": true, "expects_training_arg": true, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "preserve_input_structure_in_config": false, "autocast": true, "class_name": "Lambda", "config": {"name": "lambda_21", "trainable": true, "dtype": "float32", "function": {"class_name": "__tuple__", "items": ["4wEAAAAAAAAAAAAAAAcAAAAGAAAAQwAAAHNoAAAAfABkARkAfABkAhkAAgB9AX0CdABqAXwBfAIU\nAGQDZASNAn0DdACgAnQAagF0AKADfAGhAWQDZASNAqEBfQR0AKACdABqAXQAoAN8AqEBZANkBI0C\noQF9BXwDfAR8BRQAGwB9BnwGUwApBU7pAAAAAOkBAAAA6f////8pAdoEYXhpcykE2gFL2gNzdW3a\nBHNxcnTaBnNxdWFyZSkH2gF42gJ4MdoCeDLaC2RvdF9wcm9kdWN02gdub3JtX3gx2gdub3JtX3gy\n2hFjb3NpbmVfc2ltaWxhcml0eakAchAAAAD6IDxpcHl0aG9uLWlucHV0LTEwNC1hMmViZDUxMjI0\nZjQ+cg8AAAAEAAAAcwwAAAAAARIBEgEaARoBDAE=\n", null, null]}, "function_type": "lambda", "module": "__main__", "output_shape": null, "output_shape_type": "raw", "output_shape_module": null, "arguments": {}}, "inbound_nodes": [[["reshape_32", 0, 0, {}], ["reshape_33", 0, 0, {}]]], "shared_object_id": 4, "build_input_shape": [{"class_name": "TensorShape", "items": [null, 1024, 1]}, {"class_name": "TensorShape", "items": [null, 1024, 1]}]}2
�root.layer_with_weights-0"_tf_keras_layer*�{"name": "dense_39", "trainable": true, "expects_training_arg": false, "dtype": "float32", "batch_input_shape": null, "stateful": false, "must_restore_from_config": false, "preserve_input_structure_in_config": false, "autocast": true, "class_name": "Dense", "config": {"name": "dense_39", "trainable": true, "dtype": "float32", "units": 1, "activation": "sigmoid", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}, "shared_object_id": 5}, "bias_initializer": {"class_name": "Zeros", "config": {}, "shared_object_id": 6}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}, "inbound_nodes": [[["lambda_21", 0, 0, {}]]], "shared_object_id": 7, "input_spec": {"class_name": "InputSpec", "config": {"dtype": null, "shape": null, "ndim": null, "max_ndim": null, "min_ndim": 2, "axes": {"-1": 1024}}, "shared_object_id": 14}, "build_input_shape": {"class_name": "TensorShape", "items": [null, 1024]}}2
�]root.keras_api.metrics.0"_tf_keras_metric*�{"class_name": "Mean", "name": "loss", "dtype": "float32", "config": {"name": "loss", "dtype": "float32"}, "shared_object_id": 15}2
�^root.keras_api.metrics.1"_tf_keras_metric*�{"class_name": "MeanMetricWrapper", "name": "pearson_correlation", "dtype": "float32", "config": {"name": "pearson_correlation", "dtype": "float32", "fn": "pearson_correlation"}, "shared_object_id": 11}2
�_root.keras_api.metrics.2"_tf_keras_metric*�{"class_name": "MeanMetricWrapper", "name": "mae", "dtype": "float32", "config": {"name": "mae", "dtype": "float32", "fn": "mean_absolute_error"}, "shared_object_id": 12}2
�`root.keras_api.metrics.3"_tf_keras_metric*�{"class_name": "MeanMetricWrapper", "name": "mse", "dtype": "float32", "config": {"name": "mse", "dtype": "float32", "fn": "mean_squared_error"}, "shared_object_id": 13}2