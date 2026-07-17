(ns vocabulary-estimation.preview-html
  (:require [clojure.string :as str]))

(defn preserve-origin [html]
  (-> html
      (str/replace
       "location.assign('http://localhost:'+clay_port);"
       "location.assign(window.location.origin);")
      (str/replace
       "new WebSocket('ws://localhost:'+clay_port);"
       (str "new WebSocket((window.location.protocol === 'https:' ? 'wss://' : "
            "'ws://') + window.location.host);"))))
