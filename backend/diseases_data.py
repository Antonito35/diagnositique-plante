"""
Base de connaissances des 38 classes PlantVillage : nom français, sévérité
de référence, et recommandations de traitement (préventif / biologique /
conventionnel). L'ordre et les clés (PLANTVILLAGE_LABELS) DOIVENT correspondre
exactement à l'index de sortie du modèle entraîné (voir class_names.json).
"""

# Ordre exact des classes tel que produit par le modèle (index = position ici)
PLANTVILLAGE_LABELS = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

_MECA_ROW_CROP = (
    " Désherbage mécanique possible tant que la culture est jeune, avant la "
    "fermeture du couvert végétal ; arrêter dès que le buttage ou le feuillage "
    "dense empêche le passage de l'outil sans casser les tiges."
)
_MECA_ORCHARD = (
    " Sur le rang, un griffage ou un décavaillonnage limité à l'automne-hiver "
    "(hors période de gel et de sève montante) réduit l'inoculum au sol sans "
    "abîmer les racines superficielles."
)
_MECA_VIGNE = (
    " Travail du sol du rang (décavaillonnage, griffage) à faire avant le "
    "débourrement ou après la nouaison ; jamais pendant la floraison."
)

DISEASES_DB = {
    "Apple___Apple_scab": {
        "name_fr": "Tavelure du pommier",
        "severity": "Moderate",
        "recommendation": "Traiter dès les premières taches : la tavelure se propage vite par temps humide.",
        "treatments": {
            "preventive": "Ramasser et détruire les feuilles mortes à l'automne (le champignon y hiverne). Aérer la ramure par une taille adaptée.",
            "biological": "Pulvériser de la bouillie bordelaise (cuivre) ou du soufre dès le débourrement." + _MECA_ORCHARD,
            "conventional": "Fongicide de synthèse (strobilurine ou triazole) en programme préventif dès l'éclatement des bourgeons."
        }
    },
    "Apple___Black_rot": {
        "name_fr": "Pourriture noire du pommier",
        "severity": "Severe",
        "recommendation": "Agir vite : cette maladie détruit aussi bien les feuilles que les fruits.",
        "treatments": {
            "preventive": "Éliminer les fruits momifiés et le bois mort, sources principales de contamination.",
            "biological": "Traitement cuprique en sortie d'hiver, avant le débourrement." + _MECA_ORCHARD,
            "conventional": "Fongicide homologué contre les maladies du bois et du fruit, en programme printanier."
        }
    },
    "Apple___Cedar_apple_rust": {
        "name_fr": "Rouille grillagée du pommier",
        "severity": "Moderate",
        "recommendation": "Surveiller les genévriers à proximité : ils hébergent le champignon en hiver.",
        "treatments": {
            "preventive": "Éloigner les plantations de pommiers des genévriers (hôte alterné obligatoire du champignon).",
            "biological": "Soufre mouillable en traitement préventif au printemps." + _MECA_ORCHARD,
            "conventional": "Fongicide triazole au moment de la sortie des feuilles."
        }
    },
    "Apple___healthy": {
        "name_fr": "Pommier sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Inspection régulière du feuillage et des fruits.",
            "biological": "Aucun traitement nécessaire." + _MECA_ORCHARD,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Blueberry___healthy": {
        "name_fr": "Myrtillier sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Vérifier régulièrement le feuillage, surtout après une période humide.",
            "biological": "Aucun traitement nécessaire.",
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "name_fr": "Oïdium du cerisier",
        "severity": "Mild",
        "recommendation": "Peu grave mais à traiter rapidement pour éviter la propagation.",
        "treatments": {
            "preventive": "Assurer une bonne aération de la ramure ; éviter l'excès d'engrais azoté.",
            "biological": "Pulvériser du soufre, simple et peu coûteux." + _MECA_ORCHARD,
            "conventional": "Fongicide anti-oïdium spécifique en cas de forte pression."
        }
    },
    "Cherry_(including_sour)___healthy": {
        "name_fr": "Cerisier sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Inspection régulière du feuillage.",
            "biological": "Aucun traitement nécessaire." + _MECA_ORCHARD,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name_fr": "Cercosporiose du maïs (tache grise)",
        "severity": "Moderate",
        "recommendation": "Surveiller l'évolution, particulièrement en climat chaud et humide.",
        "treatments": {
            "preventive": "Rotation des cultures et broyage fin des résidus de récolte, qui hébergent le champignon.",
            "biological": "Pas de solution biologique très efficace ; miser sur des variétés tolérantes." + _MECA_ROW_CROP,
            "conventional": "Fongicide foliaire (strobilurine) si le seuil de nuisibilité est dépassé."
        }
    },
    "Corn_(maize)___Common_rust_": {
        "name_fr": "Rouille commune du maïs",
        "severity": "Moderate",
        "recommendation": "Traiter si les pustules progressent rapidement sur les feuilles hautes.",
        "treatments": {
            "preventive": "Privilégier des variétés résistantes ; éviter les semis trop denses.",
            "biological": "Peu de leviers biologiques directs ; renforcer la vigueur de la plante (fertilisation équilibrée)." + _MECA_ROW_CROP,
            "conventional": "Fongicide à base de triazole ou strobilurine si l'infestation est précoce et sévère."
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "name_fr": "Helminthosporiose du maïs",
        "severity": "Severe",
        "recommendation": "Traiter sans tarder : les lésions en fuseau peuvent réduire fortement le rendement.",
        "treatments": {
            "preventive": "Rotation avec une culture non-hôte et enfouissement des résidus de maïs.",
            "biological": "Variétés tolérantes en priorité ; peu de produits biologiques homologués efficaces." + _MECA_ROW_CROP,
            "conventional": "Fongicide foliaire dès l'apparition des premières lésions sur les feuilles du bas."
        }
    },
    "Corn_(maize)___healthy": {
        "name_fr": "Maïs sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière du feuillage, en particulier après un épisode pluvieux.",
            "biological": "Aucun traitement nécessaire." + _MECA_ROW_CROP,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Grape___Black_rot": {
        "name_fr": "Black-rot de la vigne",
        "severity": "Severe",
        "recommendation": "Traiter en urgence : cette maladie peut détruire toute la récolte de raisin.",
        "treatments": {
            "preventive": "Supprimer les grappes momifiées et les sarments contaminés, principales sources d'inoculum.",
            "biological": "Cuivre et soufre en programme préventif dès le débourrement." + _MECA_VIGNE,
            "conventional": "Fongicide systémique en programme, renforcé avant la floraison."
        }
    },
    "Grape___Esca_(Black_Measles)": {
        "name_fr": "Esca de la vigne",
        "severity": "Severe",
        "recommendation": "Maladie du bois grave et sans traitement curatif efficace : agir en prévention.",
        "treatments": {
            "preventive": "Tailler tardivement et par temps sec ; protéger les plaies de taille ; arracher les ceps trop atteints.",
            "biological": "Application de préparations à base de Trichoderma sur les plaies de taille." + _MECA_VIGNE,
            "conventional": "Pas de fongicide curatif homologué efficace ; la prévention reste le seul levier."
        }
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "name_fr": "Brûlure des feuilles de la vigne (Isariopsis)",
        "severity": "Moderate",
        "recommendation": "Traiter pour éviter la défoliation prématurée, néfaste à la maturation.",
        "treatments": {
            "preventive": "Effeuillage de la zone des grappes pour améliorer l'aération et l'ensoleillement.",
            "biological": "Cuivre en traitement préventif, comme pour le mildiou." + _MECA_VIGNE,
            "conventional": "Fongicide anti-mildiou classique, efficace aussi sur cette maladie."
        }
    },
    "Grape___healthy": {
        "name_fr": "Vigne saine",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière, en particulier après un épisode pluvieux.",
            "biological": "Aucun traitement nécessaire." + _MECA_VIGNE,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "name_fr": "Maladie du dragon jaune (HLB) des agrumes",
        "severity": "Severe",
        "recommendation": "Maladie très grave et incurable : signaler immédiatement aux autorités phytosanitaires.",
        "treatments": {
            "preventive": "Lutter contre le psylle vecteur (Diaphorina citri) et utiliser des plants certifiés indemnes.",
            "biological": "Auxiliaires prédateurs du psylle vecteur, en complément d'un suivi sanitaire strict.",
            "conventional": "Aucun traitement curatif : arrachage et destruction des arbres contaminés obligatoires."
        }
    },
    "Peach___Bacterial_spot": {
        "name_fr": "Tache bactérienne du pêcher",
        "severity": "Moderate",
        "recommendation": "Traiter tôt en saison, avant que la bactérie ne s'installe durablement.",
        "treatments": {
            "preventive": "Éviter l'arrosage par aspersion qui favorise la dissémination de la bactérie.",
            "biological": "Traitement cuprique en sortie d'hiver." + _MECA_ORCHARD,
            "conventional": "Bactéricide à base de cuivre, en programme renforcé si le climat est humide."
        }
    },
    "Peach___healthy": {
        "name_fr": "Pêcher sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Inspection régulière du feuillage et des jeunes pousses.",
            "biological": "Aucun traitement nécessaire." + _MECA_ORCHARD,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Pepper,_bell___Bacterial_spot": {
        "name_fr": "Tache bactérienne du poivron",
        "severity": "Moderate",
        "recommendation": "Traiter rapidement : la bactérie se propage vite par temps chaud et humide.",
        "treatments": {
            "preventive": "Utiliser des semences saines et pratiquer une rotation de 2-3 ans hors solanacées.",
            "biological": "Traitement cuprique préventif dès la plantation." + _MECA_ROW_CROP,
            "conventional": "Bactéricide cuprique en programme si les conditions restent humides."
        }
    },
    "Pepper,_bell___healthy": {
        "name_fr": "Poivron sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière du feuillage.",
            "biological": "Aucun traitement nécessaire." + _MECA_ROW_CROP,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Potato___Early_blight": {
        "name_fr": "Alternariose de la pomme de terre",
        "severity": "Moderate",
        "recommendation": "Traiter dès les premières taches en cocarde sur les feuilles basses.",
        "treatments": {
            "preventive": "Rotation longue (3-4 ans) et fertilisation azotée équilibrée (l'excès favorise la maladie).",
            "biological": "Cuivre en traitement préventif dès la levée." + _MECA_ROW_CROP,
            "conventional": "Fongicide anti-mildiou/alternariose en programme, dès les premiers symptômes."
        }
    },
    "Potato___Late_blight": {
        "name_fr": "Mildiou de la pomme de terre",
        "severity": "Severe",
        "recommendation": "Urgence : le mildiou peut détruire une parcelle entière en quelques jours par temps humide.",
        "treatments": {
            "preventive": "Buttage soigné, aération des rangs, destruction des tas de déchets de tubercules.",
            "biological": "Cuivre en traitement préventif, renouvelé après chaque pluie lessivante." + _MECA_ROW_CROP,
            "conventional": "Fongicide systémique anti-mildiou, en programme serré dès que les conditions sont favorables (humidité, douceur)."
        }
    },
    "Potato___healthy": {
        "name_fr": "Pomme de terre saine",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière, en particulier après un épisode humide.",
            "biological": "Aucun traitement nécessaire." + _MECA_ROW_CROP,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Raspberry___healthy": {
        "name_fr": "Framboisier sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Inspection régulière du feuillage et des cannes.",
            "biological": "Aucun traitement nécessaire.",
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Soybean___healthy": {
        "name_fr": "Soja sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière du feuillage.",
            "biological": "Aucun traitement nécessaire." + _MECA_ROW_CROP,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Squash___Powdery_mildew": {
        "name_fr": "Oïdium de la courge",
        "severity": "Mild",
        "recommendation": "Pas grave dans l'immédiat, mais à traiter pour préserver le feuillage.",
        "treatments": {
            "preventive": "Espacer les plants pour une bonne circulation d'air ; éviter les arrosages sur le feuillage.",
            "biological": "Pulvériser du soufre ou une solution de bicarbonate de potassium." + _MECA_ROW_CROP,
            "conventional": "Fongicide anti-oïdium en cas de progression rapide."
        }
    },
    "Strawberry___Leaf_scorch": {
        "name_fr": "Brûlure des feuilles du fraisier",
        "severity": "Moderate",
        "recommendation": "Traiter avant la floraison pour préserver la vigueur de la plante.",
        "treatments": {
            "preventive": "Supprimer les vieilles feuilles après récolte ; espacer suffisamment les plants.",
            "biological": "Traitement cuprique préventif en sortie d'hiver.",
            "conventional": "Fongicide homologué fraisier, en traitement préventif avant floraison."
        }
    },
    "Strawberry___healthy": {
        "name_fr": "Fraisier sain",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière du feuillage.",
            "biological": "Aucun traitement nécessaire.",
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
    "Tomato___Bacterial_spot": {
        "name_fr": "Tache bactérienne de la tomate",
        "severity": "Moderate",
        "recommendation": "Traiter rapidement, cette bactérie se propage vite par temps chaud et humide.",
        "treatments": {
            "preventive": "Semences saines, rotation hors solanacées, éviter l'arrosage par aspersion.",
            "biological": "Traitement cuprique préventif dès la plantation." + _MECA_ROW_CROP,
            "conventional": "Bactéricide cuprique en programme si les conditions restent humides."
        }
    },
    "Tomato___Early_blight": {
        "name_fr": "Alternariose de la tomate",
        "severity": "Moderate",
        "recommendation": "Traiter dès les premières taches en cocarde sur les feuilles basses.",
        "treatments": {
            "preventive": "Pailler le sol pour éviter les projections de terre, tuteurer pour aérer le feuillage.",
            "biological": "Cuivre en traitement préventif, renouvelé régulièrement." + _MECA_ROW_CROP,
            "conventional": "Fongicide anti-alternariose en programme dès les premiers symptômes."
        }
    },
    "Tomato___Late_blight": {
        "name_fr": "Mildiou de la tomate",
        "severity": "Severe",
        "recommendation": "Urgence : arracher et détruire les plants trop atteints pour limiter la propagation.",
        "treatments": {
            "preventive": "Aération maximale du feuillage, éviter l'arrosage du soir et les excès d'humidité.",
            "biological": "Cuivre en traitement préventif, renouvelé après chaque pluie." + _MECA_ROW_CROP,
            "conventional": "Fongicide systémique anti-mildiou dès l'annonce de conditions favorables (humidité, douceur)."
        }
    },
    "Tomato___Leaf_Mold": {
        "name_fr": "Moisissure des feuilles (cladosporiose) de la tomate",
        "severity": "Moderate",
        "recommendation": "Fréquente sous abri : aérer immédiatement pour freiner la progression.",
        "treatments": {
            "preventive": "Aérer largement les serres et tunnels ; réduire l'humidité ambiante.",
            "biological": "Pulvériser une décoction de prêle ou du cuivre à faible dose.",
            "conventional": "Fongicide anti-cladosporiose homologué sous abri."
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "name_fr": "Septoriose de la tomate",
        "severity": "Moderate",
        "recommendation": "Traiter sans attendre : cette maladie revient souvent d'une année sur l'autre.",
        "treatments": {
            "preventive": "Ne pas replanter des tomates au même endroit 3 années de suite ; enlever les débris au sol.",
            "biological": "Bouillie bordelaise en traitement préventif dès la reprise de la végétation." + _MECA_ROW_CROP,
            "conventional": "Fongicide anti-septoriose en programme si les symptômes progressent."
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "name_fr": "Acariens tétranyques de la tomate",
        "severity": "Moderate",
        "recommendation": "Traiter rapidement, surtout par temps chaud et sec, propice à leur multiplication.",
        "treatments": {
            "preventive": "Maintenir une hygrométrie suffisante ; éviter le stress hydrique des plants.",
            "biological": "Lâcher d'acariens prédateurs (Phytoseiulus persimilis), très efficace en lutte biologique.",
            "conventional": "Acaricide spécifique en cas de forte infestation, en alternant les familles chimiques."
        }
    },
    "Tomato___Target_Spot": {
        "name_fr": "Tache cible de la tomate",
        "severity": "Moderate",
        "recommendation": "Traiter dès l'apparition des taches concentriques caractéristiques.",
        "treatments": {
            "preventive": "Aérer le feuillage, éviter l'excès d'irrigation par aspersion.",
            "biological": "Cuivre en traitement préventif." + _MECA_ROW_CROP,
            "conventional": "Fongicide à large spectre en programme si la pression est forte."
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "name_fr": "Virus des feuilles jaunes en cuillère de la tomate (TYLCV)",
        "severity": "Severe",
        "recommendation": "Aucun traitement curatif : arracher et détruire les plants atteints pour limiter la propagation.",
        "treatments": {
            "preventive": "Utiliser des variétés résistantes et des plants certifiés sains ; poser des filets anti-insectes.",
            "biological": "Lutte contre l'aleurode vecteur (Bemisia tabaci) par auxiliaires prédateurs.",
            "conventional": "Aucun traitement curatif : seule la lutte contre le vecteur (insecticide ciblé) limite la propagation."
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "name_fr": "Virus de la mosaïque de la tomate",
        "severity": "Severe",
        "recommendation": "Aucun traitement curatif : arracher les plants atteints et désinfecter les outils.",
        "treatments": {
            "preventive": "Se laver les mains et désinfecter les outils entre chaque plant (virus très contagieux par contact).",
            "biological": "Aucun traitement biologique curatif ; prévention stricte uniquement.",
            "conventional": "Aucun traitement curatif : arrachage des plants contaminés obligatoire."
        }
    },
    "Tomato___healthy": {
        "name_fr": "Tomate saine",
        "severity": "Mild",
        "recommendation": "Aucune maladie détectée. Continuer la surveillance régulière.",
        "treatments": {
            "preventive": "Surveillance régulière du feuillage, en particulier sous abri.",
            "biological": "Aucun traitement nécessaire." + _MECA_ROW_CROP,
            "conventional": "Aucun traitement nécessaire pour le moment."
        }
    },
}

assert set(DISEASES_DB.keys()) == set(PLANTVILLAGE_LABELS), \
    "DISEASES_DB doit couvrir exactement les 38 labels PlantVillage"
