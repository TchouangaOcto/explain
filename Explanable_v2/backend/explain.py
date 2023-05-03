import os
from pathlib import Path
import sys
import pickle
import dalex as dx
from shapash import SmartExplainer
import shap




current_dir = os.getcwd()
current_dir = Path(Path(current_dir).parent.absolute())

# repertoire donnant accès au train model file
sys.path.append(os.path.join(current_dir, 'Model'))


# repertoire donnant accès au log file
sys.path.append(os.path.join(current_dir, 'log'))
from log import log

# référence log
file = "log/explanable.log"
logfile = os.path.join(current_dir, file)
logger = log()
log = logger.log(logfile)

class explain:
    """
    Classe créant l'instance permetant de faire l'explicabilité
    """
    def __init__(self,modèle, dataset,variable_à_predire):
        log.info('chargement du modèle')
        # try:
        #     #modelpath = f'Model_version\{modelpath}'
        #     #path = os.path.join(current_dir,modelpath)
        #     with open(model, "rb") as f:
        #         self.model = pickle.load(f)
        # except Exception as e:
        #     log.error(e)
        self.modèle =modèle
        self.dataset = dataset
        self.variable_à_predire =  variable_à_predire
        log.info("récupération des données d'entrainement")
        try:
            self.X = self.dataset.drop(self.variable_à_predire,axis=1)
            candidates = ['Unnamed: 0']
            self.X = self.X.drop([x for x in candidates if x in self.X.columns], 1)
            self.y = self.dataset[self.variable_à_predire]
            print(self.X)
        except Exception as e:
            log.error(e)
class dalex(explain):
    """
    Classe permetant de géré l'explicabilité avec dalex
    """
    def __init__(self,modèle, dataset, variable_à_predire):

            self.modèle = modèle
            self.dataset = dataset

            log.info("création de l'objet explain")
            try:
             explain.__init__(self, modèle, dataset, variable_à_predire)
            except Exception as e:
                log.error(e)

            log.info("lancement du objet d'explanabilité avec dalex")
            try:
                self.modelexpl = dx.Explainer(self.modèle, self.X, self.y)
            except Exception as e:
                log.error(e)

    def correlation_heirarchique(self):
            """
            Fonction permettant de générer les corrélations hiérarchiques entre les variables
            explicative
            :return: diagram de representation des corrélations hiérarchiques
            """
            log.info("calcule d'analyse hiérarchique des correlation entre variable")
            try:
                asp = dx.Aspect(self.modelexpl)
                return asp
            except Exception as e:
                log.error(e)

    def feature_importance(self):
            """
            Fonction permettant de générer le feature importance des
            variables explicatf
            :return: le diagramme de feature importance
            """
            log.info("calcule de feature importance")
            try:
                return self.modelexpl.model_parts(loss_function = 'rmse').plot(bar_width=30,show=False)
            except Exception as e:
                log.error(e)

    def predict_profile(self, variable):
        return self.modelexpl.predict_profile(self.X,variables=variable).plot(show=False)
    def feature_importance_shap(self,dataset): # problem With this
        """
        fonction donnant le graphique de feature importance avec les shapely values
        :return: objet de shapely
        """
        log.info("calcule de feature importance shap")
        try:
            #return self.modelexpl.predict_parts(dataset, type='shap').plot(show=False)
            return self.modelexpl.model_parts(type='shap_wrapper', shap_explainer_type="TreeExplainer").plot()
            pass
        except Exception as e:
            log.error(e)

    def feature_importance_positif_negatif(self,observation,type='shap'):
            """
            Fonction permettant de générer le feature importance basé sur les shapely values
            et la méthode de breakdown de dalex.
            :param observation: Représente une observation du jeu de donnée
            :param type: Représente la technique utilisée pour reproduire le feature importance
            :return: le diagramme de feature importance d'une observation
            """
            log.info("calcule de variable importance locale")
            try:
                return self.modelexpl.predict_parts(observation,type=type).plot(bar_width=30,show=False)
            except Exception as e:
                log.error(e)
    def analyse_heirarchiaque_et_feature_importance(self):
            """
            Fonction donnant une analyse sur la corrélation hiérarchique et individuel et corrélé et
            feature importance individuel
            :return: diagramme de corrélation hiérarchique et individuel et corrélé et
            feature importance individuel
            """
            log.info("calcule de variable importance avec analyse hierarchique")
            try:
                asp = self.correlation_heirarchique()
                return asp.model_triplot(random_state=42).plot(show=False)
            except Exception as e:
                log.error(e)
    def feature_importance_groupé(self,taux=0.05):
            """
            Fonction permettant de calculer le feature importance groupé des variables
            explicatif
            :return: diagram de feature importance groupé
            """
            log.info("calcule du feature importance groupé")
            try:
                asp = self.correlation_heirarchique()
                feaureimportancegroup = asp.model_parts(h=taux,
                                                         label=' Random forest variable gropup importance created on treshold h=0.1')
                return feaureimportancegroup.plot(show=False)
            except Exception as e:
                log.error(e)

    def pdp_ale_variable(self, variable):
            """
            Fonction permettant de calculer le partial dependence plot et accumulated local effects des
            variables explicatif
            :param model: nom du model expliquer
            :return: diagramme de partial dependence plot et accumulated local effects
            """
            log.info('calcule des partial dependence plot et accumulated local effects ')
            try:
                pdp = self.modelexpl.model_profile(type='partial', label="partial dependence plot",)
                ale = self.modelexpl.model_profile(type='accumulated', label="accumulated local effects")
                return ale.plot(pdp,variables=variable, show=False)
            except Exception as e:
                log.error(e)
    def launch_server(self):
            """
            Fonction permettant de lancer le serveur dalex pour mise en place des
            tableaux de bords
            :return: rien
            """
            log.info('launching dalex server')
            try:
                arena = dx.Arena()
                arena.push_model(self.modelexpl)
                arena.push_observations(explain.X.iloc[0:3])
                arena.run_server(port=8080)
            except Exception as e:
                log.error(e)
class shapash(explain):
    """
    Classe permetant de géré l'explicabilité avec dalex
    """
    def __init__(self,modelpath, datapath):
            log.info("création de l'objet explain")
            try:
             explain.__init__(self, modelpath, datapath)
            except Exception as e:
                log.error(e)

            log.info("chargement du module shapash")
            try:
                self.ShapExplainer = SmartExplainer(model=explain.model)
                self.ShapExplainer.compile(x=explain.X, y_target=explain.y)
            except Exception as e:
                log.error(e)
    def stabilité_globale(self):
        log.info("vue sur la stabilité global du modèle")
        try:
            stable_plot = self.ShapExplainer.plot.stability_plot()
            return stable_plot
        except Exception as e:
            log.error(e)

    def stabilité_précis(self,num_feature=5):
        log.info("stabilité locale sur un nombre restrain de variable")
        try:
            stable_plot_précis = self.ShapExplainer.plot.stability_plot(max_features=num_feature, distribution="boxplot")
            return stable_plot_précis
        except Exception as e:
            log.error(e)


#shap class
class SHAP(explain):
    """
    Classe permetant de géré l'explicabilité avec dalex
    """
    def __init__(self,modèle, dataset, variable_à_predire):

            self.modèle = modèle
            self.dataset = dataset

            log.info("création de l'objet explain")
            try:
             explain.__init__(self, modèle, dataset, variable_à_predire)
            except Exception as e:
                log.error(e)

            log.info("lancement du objet d'explanabilité avec dalex")
            try:
                self.explainer = shap.TreeExplainer(modèle)
                values = self.explainer.shap_values(self.X, self.y)
            except Exception as e:
                log.error(e)
    def global_beeswarm(self):
        return shap.plots.beeswarm(shap_values)
