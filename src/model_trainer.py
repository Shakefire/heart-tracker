import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score
from sklearn.utils.class_weight import compute_class_weight
import streamlit as st


class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.history = {}

    def create_cnn_model(self, input_shape, num_classes=2):
        """Create CNN model for tabular data"""
        output_units = 1 if num_classes == 2 else num_classes
        activation = 'sigmoid' if num_classes == 2 else 'softmax'
        model = keras.Sequential([
            layers.Reshape((input_shape[0], 1), input_shape=input_shape),
            layers.Conv1D(32, 3, activation='relu'),
            layers.Conv1D(64, 3, activation='relu'),
            layers.MaxPooling1D(2),
            layers.Conv1D(128, 3, activation='relu'),
            layers.GlobalMaxPooling1D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(output_units, activation=activation)
        ])
        return model

    def create_lstm_model(self, input_shape, num_classes=2):
        """Create LSTM model for tabular data"""
        output_units = 1 if num_classes == 2 else num_classes
        activation = 'sigmoid' if num_classes == 2 else 'softmax'
        model = keras.Sequential([
            layers.Reshape((input_shape[0], 1), input_shape=input_shape),
            layers.LSTM(64, return_sequences=True),
            layers.Dropout(0.3),
            layers.LSTM(32),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(output_units, activation=activation)
        ])
        return model

    def create_cnn_lstm_model(self, input_shape, num_classes=2):
        """Create CNN-LSTM hybrid model"""
        output_units = 1 if num_classes == 2 else num_classes
        activation = 'sigmoid' if num_classes == 2 else 'softmax'
        model = keras.Sequential([
            layers.Reshape((input_shape[0], 1), input_shape=input_shape),
            layers.Conv1D(32, 3, activation='relu'),
            layers.Conv1D(64, 3, activation='relu'),
            layers.MaxPooling1D(2),
            layers.LSTM(50, return_sequences=True),
            layers.LSTM(25),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(output_units, activation=activation)
        ])
        return model

    def create_dnn_model(self, input_shape, num_classes=2):
        """Create Deep Neural Network model"""
        output_units = 1 if num_classes == 2 else num_classes
        activation = 'sigmoid' if num_classes == 2 else 'softmax'
        model = keras.Sequential([
            layers.Dense(256, activation='relu', input_shape=input_shape),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.1),
            layers.Dense(output_units, activation=activation)
        ])
        return model

    def compile_model(self, model, num_classes=2):
        """Compile model with appropriate loss and metrics"""
        if num_classes == 2:
            loss = 'binary_crossentropy'
            metrics = ['accuracy']
        else:
            loss = 'sparse_categorical_crossentropy'
            metrics = ['accuracy']

        model.compile(
            optimizer='adam',
            loss=loss,
            metrics=metrics
        )
        return model

    def train_model(self, model, X_train, y_train, X_test, y_test, epochs=50, batch_size=32):
        """Train a single model"""
        # Calculate class weights for imbalanced data
        class_weights = compute_class_weight(
            'balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        class_weight_dict = dict(enumerate(class_weights))

        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6
            )
        ]

        # Train model
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            class_weight=class_weight_dict,
            callbacks=callbacks,
            verbose=0
        )

        return history

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate model and return metrics"""
        # Predictions
        y_pred_proba = model.predict(X_test, verbose=0)

        if len(y_pred_proba.shape) > 1 and y_pred_proba.shape[1] > 1:
            y_pred = np.argmax(y_pred_proba, axis=1)
            # Probability of positive class
            y_pred_proba_pos = y_pred_proba[:, 1]
        else:
            y_pred_proba_pos = y_pred_proba.flatten()
            y_pred = (y_pred_proba_pos > 0.5).astype(int)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc_roc = roc_auc_score(y_test, y_pred_proba_pos)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        return {
            'accuracy': accuracy,
            'auc_roc': auc_roc,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }

    def train_all_models(self, X_train, y_train, X_test, y_test):
        """Train all models and return results"""
        input_shape = X_train.shape[1:]
        num_classes = len(np.unique(y_train))

        # Convert to categorical if binary
        if num_classes == 2:
            y_train_cat = y_train
            y_test_cat = y_test
        else:
            y_train_cat = keras.utils.to_categorical(y_train, num_classes)
            y_test_cat = keras.utils.to_categorical(y_test, num_classes)

        models_to_train = {
            'CNN': self.create_cnn_model,
            'LSTM': self.create_lstm_model,
            'CNN-LSTM': self.create_cnn_lstm_model,
            'DNN': self.create_dnn_model
        }

        results = {}

        for model_name, model_func in models_to_train.items():
            st.write(f"Training {model_name}...")

            # Create and compile model
            model = model_func(input_shape, num_classes)
            model = self.compile_model(model, num_classes)

            # Train model
            history = self.train_model(
                model, X_train, y_train_cat, X_test, y_test_cat
            )

            # Evaluate model
            metrics = self.evaluate_model(model, X_test, y_test)

            # Store results
            self.models[model_name] = model
            self.history[model_name] = history
            results[model_name] = metrics

            st.write(
                f"✅ {model_name} - Accuracy: {metrics['accuracy']:.3f}, AUC-ROC: {metrics['auc_roc']:.3f}")

        return self.models, results

    def get_best_model(self, results):
        """Get the best performing model based on AUC-ROC"""
        best_model_name = max(
            results.keys(), key=lambda x: results[x]['auc_roc'])
        return best_model_name, self.models[best_model_name]

    def save_models(self, filepath_prefix):
        """Save all trained models"""
        for model_name, model in self.models.items():
            filepath = f"{filepath_prefix}_{model_name.lower().replace('-', '_')}.h5"
            model.save(filepath)
            st.write(f"Model {model_name} saved to {filepath}")

    def load_models(self, filepath_prefix):
        """Load saved models"""
        model_names = ['CNN', 'LSTM', 'CNN-LSTM', 'DNN']

        for model_name in model_names:
            filepath = f"{filepath_prefix}_{model_name.lower().replace('-', '_')}.h5"
            try:
                self.models[model_name] = keras.models.load_model(filepath)
                st.write(f"Model {model_name} loaded from {filepath}")
            except:
                st.warning(
                    f"Could not load model {model_name} from {filepath}")

        return self.models
