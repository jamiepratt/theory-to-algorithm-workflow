(ns vocabulary-estimation.preview-html-test
  (:require [clojure.test :refer [deftest is testing]]
            [vocabulary-estimation.preview-html :as preview-html]))

(def clay-live-reload-html
  (str "<main>article</main><script>"
       "location.assign('http://localhost:'+clay_port);"
       "const socket = new WebSocket('ws://localhost:'+clay_port);"
       "</script>"))

(deftest preserve-origin-test
  (let [html (preview-html/preserve-origin clay-live-reload-html)]
    (testing "reload and websocket stay on the current page origin"
      (is (re-find #"location\.assign\(window\.location\.origin\)" html))
      (is (re-find #"window\.location\.protocol" html))
      (is (re-find #"window\.location\.host" html))
      (is (not (re-find #"http://localhost" html)))
      (is (not (re-find #"ws://localhost" html))))
    (testing "article content is unchanged"
      (is (re-find #"<main>article</main>" html)))))
