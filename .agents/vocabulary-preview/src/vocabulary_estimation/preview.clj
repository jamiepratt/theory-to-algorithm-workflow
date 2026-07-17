(ns vocabulary-estimation.preview
  (:gen-class)
  (:require [civitas.db :as db]
            [clojure.java.io :as io]
            [clojure.string :as str]
            [ring.util.mime-type :as mime-type]
            [vocabulary-estimation.preview-html :as preview-html]
            [scicloj.clay.v2.main :as clay-main]
            [scicloj.clay.v2.server :as clay-server]
            [scicloj.clay.v2.server.state :as server-state]
            [scicloj.kindly.v4.api :as kindly])
  (:import (java.io File)))

(def default-preview-source
  "language_learning/vocabulary_estimation/bayes_theorem_simulations.clj")

(def preview-root "temp")
(def published-root "site/_site")

(def clay-wrap-html clay-server/wrap-html)

(def preview-config
  {:watch-dirs ["src"]
   :format [:quarto :html]
   :run-quarto true
   :browse false
   :config/transform 'vocabulary-estimation.preview/expand-preview-config})

(defn- ns-clay-config [ns-form]
  (let [[_ sym ?doc ?attr] ns-form]
    (kindly/deep-merge
     (some-> ns-form meta :clay)
     (some-> sym meta :clay)
     (:clay (cond
              (map? ?doc) ?doc
              (map? ?attr) ?attr)))))

(defn expand-preview-config [config]
  (let [quarto (:quarto config)
        ns-quarto (some-> config :ns-form ns-clay-config :quarto)]
    (db/expand-authors
     (if (and ns-quarto (-> quarto meta :replace))
       (assoc config :quarto
              (kindly/deep-merge ns-quarto (with-meta quarto nil)))
       config))))

(defn- regular-file-under [root uri]
  (when (and (string? uri) (str/starts-with? uri "/"))
    (let [root-file (.getCanonicalFile (io/file root))
          file (.getCanonicalFile (io/file root-file (subs uri 1)))
          root-prefix (str (.getPath root-file) File/separator)]
      (when (and (str/starts-with? (.getPath file) root-prefix)
                 (.isFile file))
        file))))

(defn- current-preview-uri []
  (let [{:keys [base-target-path full-target-path]}
        (:last-rendered-spec @server-state/*state)]
    (when (and base-target-path full-target-path)
      (str "/" (clay-server/relative-url-path base-target-path
                                              full-target-path)))))

(defn preview-fallback-handler [{:keys [request-method uri]}]
  (let [preview-file (regular-file-under preview-root uri)
        linked-html? (and (str/ends-with? uri ".html")
                          (not= uri (current-preview-uri)))]
    (when (and (= :get request-method)
               (or (nil? preview-file) linked-html?))
      (when-let [file (regular-file-under published-root uri)]
        {:status 200
         :headers {"Content-Type"
                   (or (mime-type/ext-mime-type uri)
                       "application/octet-stream")}
         :body (if (str/ends-with? uri ".html")
                 (clay-server/wrap-html (slurp file) @server-state/*state)
                 file)}))))

(defn args-with-preview-config [args]
  (into ["--config-map" (pr-str preview-config)]
        (if (seq args)
          args
          [default-preview-source])))

(defn- install-origin-preserving-wrapper! []
  (alter-var-root
   #'clay-server/wrap-html
   (constantly
    (fn [html state]
      (preview-html/preserve-origin
       (clay-wrap-html html state))))))

(defn -main [& args]
  (install-origin-preserving-wrapper!)
  (clay-server/install-handler! #'preview-fallback-handler)
  (apply clay-main/-main (args-with-preview-config args)))
