variable "public_key_path" {
  description = "The path to the public key to be used for SSH access"
  type = string
  default = "~/.ssh/id_rsa.pub"
}