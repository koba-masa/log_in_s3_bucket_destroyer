# インフラ環境

## 環境構築

### システム構築

- 新規作成

```sh
aws cloudformation create-stack --stack-name log-in-s3-bucket-destroyer \
   --capabilities CAPABILITY_NAMED_IAM \
   --template-body file://main.yaml
```

- 更新

```sh
aws cloudformation update-stack --stack-name log-in-s3-bucket-destroyer \
  --capabilities CAPABILITY_NAMED_IAM \
  --template-body file://main.yaml
```

- 削除

```sh
aws cloudformation delete-stack --stack-name log-in-s3-bucket-destroyer
```

### デプロイ用ユーザー

```sh
aws cloudformation create-stack --stack-name log-in-s3-bucket-destroyer-deployer \
   --capabilities CAPABILITY_NAMED_IAM \
   --template-body file://deploy_user.yaml
```

- 更新

```sh
aws cloudformation update-stack --stack-name log-in-s3-bucket-destroyer-deployer \
  --capabilities CAPABILITY_NAMED_IAM \
  --template-body file://deploy_user.yaml
```

- 削除

```sh
aws cloudformation delete-stack --stack-name log-in-s3-bucket-destroyer-deployer
```
