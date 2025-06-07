import numpy as np
import pandas as pd
import lime
from lime.lime_tabular import LimeTabularExplainer
import streamlit as st
from sklearn.base import BaseEstimator, ClassifierMixin

class KerasClassifierWrapper(BaseEstimator, ClassifierMixin):
    """Wrapper for Keras models to work with LIME"""
    
    def __init__(self, model):
        self.model = model
        self.classes_ = np.array([0, 1])
    
    def predict_proba(self, X):
        """Predict class probabilities"""
        predictions = self.model.predict(X, verbose=0)
        
        # Debug: log shapes
        # print(f"Predictions shape: {predictions.shape}")
        
        if len(predictions.shape) == 1:
            # Binary classification with sigmoid output
            proba_positive = predictions.flatten()
            proba_negative = 1 - proba_positive
            proba = np.column_stack((proba_negative, proba_positive))
            # Debug: log shape of proba
            # print(f"Proba shape after stacking: {proba.shape}")
            return proba
        elif len(predictions.shape) == 2 and predictions.shape[1] == 1:
            # Handle case where output shape is (n,1) for binary sigmoid
            proba_positive = predictions.flatten()
            proba_negative = 1 - proba_positive
            proba = np.column_stack((proba_negative, proba_positive))
            # Debug: log shape of proba
            # print(f"Proba shape after stacking (n,1): {proba.shape}")
            return proba
        else:
            # Multi-class or binary with softmax output
            return predictions
    
    def predict(self, X):
        """Predict classes"""
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)

class HeartDiseasePredictor:
    def __init__(self, models, preprocessor):
        self.models = models
        self.preprocessor = preprocessor
        self.lime_explainer = None
        self._initialize_lime_explainer()
    
    def _initialize_lime_explainer(self):
        """Initialize LIME explainer with training data"""
        try:
            # Create sample training data for LIME
            # In production, you would use actual training data
            np.random.seed(42)
            n_features = len(self.preprocessor.get_feature_names())
            sample_data = np.random.randn(100, n_features)
            
            feature_names = self.preprocessor.get_feature_names()
            
            self.lime_explainer = LimeTabularExplainer(
                sample_data,
                feature_names=feature_names,
                class_names=['Low Risk', 'High Risk'],
                mode='classification'
            )
        except Exception as e:
            st.warning(f"Could not initialize LIME explainer: {e}")
            self.lime_explainer = None
    
    def predict_risk(self, input_data, model_name='DNN'):
        """Predict heart disease risk for given input"""
        try:
            # Prepare input
            input_processed = self.preprocessor.prepare_input_for_prediction(input_data)
            
            # Get model
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            model = self.models[model_name]
            
            # Make prediction
            prediction_proba = model.predict(input_processed, verbose=0)
            
            # Handle different shapes of prediction output robustly
            if np.isscalar(prediction_proba):
                # Scalar output
                risk_probability = float(prediction_proba)
                risk_class = int(risk_probability > 0.5)
            elif isinstance(prediction_proba, (list, np.ndarray)):
                prediction_proba = np.array(prediction_proba)
                if prediction_proba.ndim == 0:
                    # Zero-dimensional array (scalar)
                    risk_probability = float(prediction_proba)
                    risk_class = int(risk_probability > 0.5)
                elif prediction_proba.ndim == 1:
                    # 1D array
                    if prediction_proba.size == 1:
                        risk_probability = float(prediction_proba[0])
                        risk_class = int(risk_probability > 0.5)
                    else:
                        # Multiple probabilities, take second class if possible
                        if prediction_proba.size > 1:
                            risk_probability = float(prediction_proba[1])
                            risk_class = int(np.argmax(prediction_proba))
                        else:
                            risk_probability = float(prediction_proba[0])
                            risk_class = int(risk_probability > 0.5)
                elif prediction_proba.ndim == 2:
                    if prediction_proba.shape[1] == 1:
                        risk_probability = float(prediction_proba[0][0])
                        risk_class = int(risk_probability > 0.5)
                    elif prediction_proba.shape[1] > 1:
                        risk_probability = float(prediction_proba[0][1])
                        risk_class = int(np.argmax(prediction_proba[0]))
                    else:
                        risk_probability = float(prediction_proba[0][0])
                        risk_class = int(risk_probability > 0.5)
                else:
                    # Unexpected shape fallback
                    risk_probability = float(prediction_proba.flat[0])
                    risk_class = int(risk_probability > 0.5)
            else:
                # Unknown type fallback
                risk_probability = float(prediction_proba)
                risk_class = int(risk_probability > 0.5)
            
            # Determine risk level
            if risk_probability < 0.3:
                risk_level = "Low"
                risk_color = "green"
            elif risk_probability < 0.7:
                risk_level = "Medium"
                risk_color = "orange"
            else:
                risk_level = "High"
                risk_color = "red"
            
            return {
                'risk_class': risk_class,
                'risk_probability': risk_probability,
                'risk_level': risk_level,
                'risk_color': risk_color,
                'model_used': model_name
            }
            
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")
            return None
    
    def explain_prediction(self, input_data, model_name='DNN', num_features=10):
        """Generate LIME explanation for the prediction"""
        try:
            if self.lime_explainer is None:
                return None
            
            # Prepare input
            input_processed = self.preprocessor.prepare_input_for_prediction(input_data)
            
            # Get model
            model = self.models[model_name]
            wrapped_model = KerasClassifierWrapper(model)
            
            # Generate explanation
            explanation = self.lime_explainer.explain_instance(
                input_processed[0],
                wrapped_model.predict_proba,
                num_features=num_features
            )
            
            return explanation
            
        except Exception as e:
            st.warning(f"Could not generate explanation: {str(e)}")
            return None
    
    def get_feature_importance(self, explanation):
        """Extract feature importance from LIME explanation"""
        if explanation is None:
            return None
        
        try:
            feature_importance = explanation.as_list()
            
            # Convert to DataFrame for easier handling
            importance_df = pd.DataFrame(feature_importance, columns=['Feature', 'Importance'])
            importance_df['Abs_Importance'] = abs(importance_df['Importance'])
            importance_df = importance_df.sort_values('Abs_Importance', ascending=False)
            
            return importance_df
            
        except Exception as e:
            st.warning(f"Could not extract feature importance: {str(e)}")
            return None
    
    def predict_all_models(self, input_data):
        """Get predictions from all available models"""
        predictions = {}
        
        for model_name in self.models.keys():
            try:
                pred = self.predict_risk(input_data, model_name)
                if pred:
                    predictions[model_name] = pred
            except Exception as e:
                st.warning(f"Error predicting with {model_name}: {str(e)}")
        
        return predictions
    
    def get_model_comparison(self, input_data):
        """Compare predictions across all models"""
        predictions = self.predict_all_models(input_data)
        
        if not predictions:
            return None
        
        # Create comparison DataFrame
        comparison_data = []
        for model_name, pred in predictions.items():
            comparison_data.append({
                'Model': model_name,
                'Risk Level': pred['risk_level'],
                'Risk Probability': pred['risk_probability'],
                'Risk Class': pred['risk_class']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        return comparison_df
    
    def get_ensemble_prediction(self, input_data):
        """Get ensemble prediction by averaging all models"""
        predictions = self.predict_all_models(input_data)
        
        if not predictions:
            return None
        
        # Average probabilities
        avg_probability = np.mean([pred['risk_probability'] for pred in predictions.values()])
        
        # Determine ensemble risk level
        if avg_probability < 0.3:
            risk_level = "Low"
            risk_color = "green"
        elif avg_probability < 0.7:
            risk_level = "Medium"
            risk_color = "orange"
        else:
            risk_level = "High"
            risk_color = "red"
        
        return {
            'risk_class': int(avg_probability > 0.5),
            'risk_probability': avg_probability,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'model_used': 'Ensemble',
            'individual_predictions': predictions
        }
