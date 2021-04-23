# 使用 Pulumi 與 OpenScap 建置稽核主機，對遠端主機進行弱點掃描

本專案將使用 GCP 作為雲端平台，並且建置下述規格的虛擬主機兩台，作為範例場景之用。

| resource type | value      |
| ------------- | ---------- |
| Instance type | e2-small   |
| Region        | asia-east1 |
| network       | standard   |

## 前置準備

* 請安裝 [gcloud SDK](https://cloud.google.com/sdk/docs/install#deb)
* Python 3.7+ :warning: 請勿安裝2.x的版本
* [Pulumi](https://www.pulumi.com/docs/get-started/install/)

:mega: 
1. 本專案所有操作都是基於 **LINUX**;
2. 如果是 Windows 的使用者，一些操作指令可能不適用! 請稍加調適;
3. gcloud與pulumi的設置請參考官網。

## 開始使用本專案

1. 下載專案原始碼，並且鍵入下述指令建立運行環境

    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip3 install -r requirements.txt
    ```
    
2.  建立 Pulumi Stack 並且設定 GCP 環境變數

    ```
    $ pulumi stack init dev
    $ pulumi config set gcp:project YOURGOOGLECLOUDPROJECT
    $ pulumi config set gcp:zone asia-east1-a
    ```

3.  進行建置 `pulumi up `
4.  請透過 google console 登入 policy server
5.  下載 SSG，並且進行檢測

    ```
    $sudo su auditor
    $cd ~
    $wget https://github.com/ComplianceAsCode/content/releases/download/v0.1.55/scap-security-guide-0.1.55.zip
    $unzip scap-security-guide-0.1.55.zip
    $oscap-ssh auditor@<client-internal-ip> 22 xccdf eval --profile xccdf_org.ssgproject.content_profile_standard --report ~/standardcheck-round1.html ~/scap-security-guide-0.1.55/ssg-ubuntu1804-ds-1.2.xml
    ```
6.  測試 ansible 腳本進行自動設定，以便消除失敗項目

    ```
    $cd ~/scap-security-guide-0.1.55/ansible
    $ansible-playbook -i "<client-internal-ip>," ubuntu1804-playbook-standard.yml -b -u auditor
    ```

7.  測試完畢後，請務必刪除相關資源，避免產生不必要的費用支出。

    ```
    $ pulumi destroy
    $ pulumi stack rm
    ```

